class ResponseObject(object):
    def __init__(self, json):
        self.json = json

    def __getattr__(self, name):
        if name in self.fields():
            return self.json.get(name)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    @classmethod
    def __dir__(cls):
        d = set(dir(cls) + cls.fields())
        d.remove('fields')

        return sorted(d)


class SessionResponseObject(ResponseObject):
    def __init__(self, session, json):
        super(SessionResponseObject, self).__init__(json)

        self.session = session


class LazyResponseObject(object):
    def __init__(self, session, id, obj_type):
        self.session = session
        self.id = id
        self._obj_type = obj_type

        self.json = None

    def __getattr__(self, name):
        return getattr(self._delegate, name)

    @property
    def _delegate(self):
        if not self.json:
            self.json = self._load()

        return self._obj_type(self.session, self.json)

    def _load(self):
        raise NotImplementedError

    def __dir__(self):
        d = set(dir(self.__class__) + self._obj_type.__dir__())

        return sorted(d)
