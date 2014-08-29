import pytest
from test.response import DummyLazyResponseObject


def test_should_get_id():
    response = DummyLazyResponseObject(None, 'id123')

    assert response.id == 'id123'

    assert response.load_count == 0


def test_should_not_load_unless_needed():
    response = DummyLazyResponseObject(None, 'id123')

    assert response.foo == 'foo-value'

    assert response.load_count == 0


def test_should_delegate_via_loader():
    response = DummyLazyResponseObject(None, 'id123')

    assert response.bar == 'bar-value'

    assert response.load_count == 1


def test_should_not_call_loader_multiple_times():
    response = DummyLazyResponseObject(None, 'id123')

    assert response.bar == 'bar-value'
    assert response.bar == 'bar-value'

    assert response.load_count == 1


def test_should_not_call_loader_on_unknown_property():
    response = DummyLazyResponseObject(None, 'id123')

    with pytest.raises(AttributeError):
        _ = response.baz

    assert response.load_count == 0


def test_should_return_valid_dir():
    response = DummyLazyResponseObject(None, 'id123')

    filtered_dir = [d for d in dir(response) if not d.startswith('_')]
    assert filtered_dir == ['bar', 'foo', 'load_count']

    assert response.load_count == 0
