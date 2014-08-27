class ResponseObject(object):
    def __init__(self, session, json):
        self.session = session
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


class LazyResponseObject(object):
    def __init__(self, id, loader, response_type):
        self.id = id
        self.loader = loader
        self.response_type = response_type

        self.delegate = None

    def __getattr__(self, name):
        if not self.delegate:
            self.delegate = self.loader()

        return getattr(self.delegate, name)

    def __dir__(self):
        return sorted(set(self.response_type.__dir__() + ['id']))