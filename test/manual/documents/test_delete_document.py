from test import get_user_session, cassette
from test.resources.documents import create_document, delete_all_documents


def test_should_delete_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/delete_document/delete_document.yaml'):
        doc = create_document(session)
        doc.delete()

        page = session.documents.list()
        assert not page.items
