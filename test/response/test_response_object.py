import pytest
from mendeley.response import ResponseObject


class DummyResponseObject(ResponseObject):
    @property
    def foo(self):
        return 'foo-value'

    @classmethod
    def fields(cls):
        return ['bar']


def test_should_get_property():
    response = DummyResponseObject(None, None)

    assert response.foo == 'foo-value'


def test_should_get_json_value():
    json = {'bar': 'bar-value'}
    response = DummyResponseObject(None, json)

    assert response.bar == 'bar-value'


def test_should_raise_error_on_unknown_value():
    json = {'bar': 'bar-value'}
    response = DummyResponseObject(None, json)

    with pytest.raises(AttributeError) as ex_info:
        _ = response.baz

    assert ex_info.value.args == ("'DummyResponseObject' object has no attribute 'baz'",)


def test_should_return_valid_dir():
    response = DummyResponseObject(None, None)

    filtered_dir = [d for d in dir(response) if not d.startswith('__')]
    assert filtered_dir == ['bar', 'foo']