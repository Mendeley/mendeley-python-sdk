from test import cassette
from test.resources.documents import *


def test_should_create_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_document/create_document.yaml'):
        doc = create_document(session)

        assert_core_document(doc)
        assert_bib_document(doc)
        assert_client_document(doc)
        assert_tags_document(doc)


def test_should_create_minimal_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_document/create_minimal_document.yaml'):
        doc = session.documents.create('Underwater basket weaving', 'journal')

        assert doc.title == 'Underwater basket weaving'
        assert doc.type == 'journal'


def test_should_create_document_with_string_accessed():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_document/create_document_string_accessed.yaml'):
        doc = session.documents.create('Underwater basket weaving', 'journal', accessed='2014-09-03')

        assert doc.title == 'Underwater basket weaving'
        assert doc.type == 'journal'
        assert doc.accessed == arrow.get(2014, 9, 3)
