from test import get_user_session, cassette
from test.resources.documents import create_document, assert_core_document, delete_all_documents


def test_should_create_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_document/create_document.yaml'):
        doc = create_document(session)

        assert_core_document(doc)
