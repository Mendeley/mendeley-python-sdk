from mendeley.response import LazyResponseObject, SessionResponseObject


class DummyResponseObject(SessionResponseObject):
    @property
    def foo(self):
        return 'foo-value'

    @classmethod
    def fields(cls):
        return ['bar']


class DummyLazyResponseObject(LazyResponseObject):
    def __init__(self, session, id):
        super(DummyLazyResponseObject, self).__init__(session, id, DummyResponseObject, lambda: self._load())

    load_count = 0

    def _load(self):
        self.load_count += 1
        return DummyResponseObject(self.session, {'bar': 'bar-value'})
