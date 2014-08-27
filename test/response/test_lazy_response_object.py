from mock import Mock

from mendeley.response import LazyResponseObject
from test.response import DummyResponseObject


def test_should_get_id():
    loader = Mock()

    response = LazyResponseObject('id123', loader, DummyResponseObject)

    assert response.id == 'id123'
    assert not loader.called


def test_should_delegate_via_loader():
    delegate = Mock()
    delegate.foo = 'foo-value'

    loader = Mock()
    loader.return_value = delegate

    response = LazyResponseObject('id123', loader, DummyResponseObject)

    assert response.foo == 'foo-value'
    assert loader.call_count == 1


def test_should_not_call_loader_multiple_times():
    delegate = Mock()
    delegate.foo = 'foo-value'
    delegate.bar = 'bar-value'

    loader = Mock()
    loader.return_value = delegate

    response = LazyResponseObject('id123', loader, DummyResponseObject)

    assert response.foo == 'foo-value'
    assert response.bar == 'bar-value'
    assert loader.call_count == 1


def test_should_return_valid_dir():
    loader = Mock()

    response = LazyResponseObject('id123', loader, DummyResponseObject)

    filtered_dir = [d for d in dir(response) if not d.startswith('__')]
    assert filtered_dir == ['bar', 'foo', 'id']

    assert not loader.called