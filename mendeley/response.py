class ResponseObject(object):
    def __init__(self, session, json):
        self.session = session
        self.json = json

    def __getattr__(self, name):
        if name in self.fields():
            return self.json.get(name)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    def __dir__(self):
        d = set(dir(type(self)) + self.fields())
        d.remove('fields')

        return sorted(d)
