class ResponseObject(object):
    """
    Base class for model classes that are returned as JSON from the API.

    Subclasses should override the `fields` method to include a list of fields that should be returned directly from the
    JSON (strings, numbers and booleans).  More complex fields will generally have a method to read the raw value from
    the JSON and parse it, annotated with `@property`.

    :param json: raw JSON returned from the API.
    """
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

    @classmethod
    def fields(cls):
        return []


class SessionResponseObject(ResponseObject):
    """
    Model class that also keeps track of a session.  This is useful for cases where related objects need to be retrieved
    on demand.

    :param session: a :class:`MendeleySession <mendeley.session.MendeleySession>`.
    :param json: raw JSON returned from the API.
    """
    def __init__(self, session, json):
        super(SessionResponseObject, self).__init__(json)

        self.session = session


class LazyResponseObject(object):
    """
    Model class that is instantiated only with an ID, and whose other fields are loaded only when required.  This
    loading is performed once only, and the results are stored for future access to fields on this object.

    This is useful when a JSON response contains an ID of a related object.  Loading the object on demand means that
    clients that only need the ID don't have to make the extra API calls.

    :param session: a :class:`MendeleySession <mendeley.session.MendeleySession>`.
    :param id: the ID of the object.
    :param obj_type: a model class representing the object type that this :class:`mendeley.response.LazyResponseObject`
    wraps.  This should be a subclass of :class:`mendeley.response.ResponseObject`.
    :param loader: a no-arg function that loads the object, returning a :class:`mendeley.response.ResponseObject`.
    """
    def __init__(self, session, id, obj_type, loader):
        self.session = session
        self.id = id

        self._obj_type = obj_type
        self._loader = loader

        self._value = None

    def __getattr__(self, name):
        return getattr(self._delegate, name)

    @property
    def _delegate(self):
        if not self._value:
            self._value = self._loader()

        return self._value

    def __dir__(self):
        d = set(dir(self.__class__) + self._obj_type.__dir__())

        return sorted(d)
