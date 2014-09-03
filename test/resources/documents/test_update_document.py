from test import cassette
from test.resources.documents import *


def test_should_update_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/update_document/update_document.yaml'):
        doc = create_document(session)
        patched_doc = doc.update(title='Overground bucket sawing')

        assert patched_doc.title == 'Overground bucket sawing'
        assert session.documents.get(doc.id).title == 'Overground bucket sawing'


def test_should_not_change_on_empty_update():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/update_document/empty_update.yaml'):
        doc = create_document(session)
        patched_doc = doc.update()

        assert_all_document(patched_doc)
        assert_all_document(session.documents.get(doc.id, view='all'))
