from test import cassette
from test.resources.documents import *


def test_should_restore_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/restore_from_trash/restore_document.yaml'):
        created_doc = create_document(session)
        trashed_doc = created_doc.move_to_trash()

        restored_doc = trashed_doc.restore()
        assert_core_document(restored_doc)

        doc = session.documents.get(created_doc.id)
        assert_core_document(doc)
