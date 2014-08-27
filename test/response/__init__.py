from mendeley.response import ResponseObject


class DummyResponseObject(ResponseObject):
    @property
    def foo(self):
        return 'foo-value'

    @classmethod
    def fields(cls):
        return ['bar']