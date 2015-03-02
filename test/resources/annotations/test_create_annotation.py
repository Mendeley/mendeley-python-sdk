from test import get_user_session, cassette
from test.resources.documents import create_document


def test_should_add_annotation():
    session = get_user_session()

    with cassette('fixtures/resources/annotations/add_annotation/add_annotation.yaml'):
        doc = create_document(session)

        annotation = doc.add_annotation("A nice annotation")

        assert annotation.text == "A nice annotation"
