from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


def test_should_delete_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/delete_document/delete_document.yaml'):
        doc = create_document(session)
        trashed_doc = doc.move_to_trash()
        trashed_doc.delete()

        page = session.trash.list()
        assert not page.items
