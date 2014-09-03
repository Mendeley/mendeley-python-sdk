from test import get_user_session, cassette
from test.resources.documents import create_document, assert_core_document, delete_all_documents


def test_should_list_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/list_documents.yaml'):
        create_document(session)

        page = session.documents.list()
        assert len(page.items) == 1
        assert page.count == 1

        assert_core_document(page.items[0])
