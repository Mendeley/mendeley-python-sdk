from mendeley.response import ResponseObject, LazyLoader


class DummyResponseObject(ResponseObject):
    @property
    def foo(self):
        return 'foo-value'

    @classmethod
    def fields(cls):
        return ['bar']


class DummyLazyResponseObject(LazyLoader, DummyResponseObject):
    load_count = 0

    def _load(self):
        self.load_count += 1
        return {'bar': 'bar-value'}