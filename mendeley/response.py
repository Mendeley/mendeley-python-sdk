class ResponseObject(object):
    def __init__(self, session, json):
        self.session = session
        self._json = json

    def __getattr__(self, name):
        if name in self.fields():
            return self._json.get(name)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    @classmethod
    def __dir__(cls):
        d = set(dir(cls) + cls.fields())
        d.remove('fields')

        return sorted(d)


class LazyLoader(object):
    def __init__(self, session, id):
        self.session = session
        self.id = id
        self.loaded_json = None

    @property
    def _json(self):
        if not self.loaded_json:
            self.loaded_json = self._load()

        return self.loaded_json

    def _load(self):
        raise NotImplementedError
