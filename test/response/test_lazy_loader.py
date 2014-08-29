from test.response import DummyLazyResponseObject, DummyResponseObject


def test_should_get_id():
    response = DummyLazyResponseObject(None, 'id123', DummyResponseObject)

    assert response.id == 'id123'

    assert response.load_count == 0


def test_should_delegate_to_method():
    response = DummyLazyResponseObject(None, 'id123', DummyResponseObject)

    assert response.foo == 'foo-value'

    assert response.load_count == 1


def test_should_delegate_to_field():
    response = DummyLazyResponseObject(None, 'id123', DummyResponseObject)

    assert response.bar == 'bar-value'

    assert response.load_count == 1


def test_should_not_call_loader_multiple_times():
    response = DummyLazyResponseObject(None, 'id123', DummyResponseObject)

    assert response.bar == 'bar-value'
    assert response.bar == 'bar-value'

    assert response.load_count == 1


def test_should_return_valid_dir():
    response = DummyLazyResponseObject(None, 'id123', DummyResponseObject)

    filtered_dir = [d for d in dir(response) if not d.startswith('_')]
    assert filtered_dir == ['bar', 'foo', 'load_count']

    assert response.load_count == 0
