from test import cassette
from test.resources.documents import *


def test_should_create_group_document():
    session = get_user_session()
    delete_all_group_documents()

    with cassette('fixtures/resources/documents/create_group_document/create_group_document.yaml'):
        doc = create_group_document(session)

        assert_core_document(doc)
        assert_bib_document(doc)
        assert_client_document(doc)
        assert_tags_document(doc)

        assert doc.group.id == '164d48fb-2343-332d-b566-1a4884a992e4'


def test_should_create_minimal_group_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_group_document/create_minimal_group_document.yaml'):
        doc = session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').documents\
            .create('Underwater basket weaving', 'journal')

        assert doc.title == 'Underwater basket weaving'
        assert doc.type == 'journal'

        assert doc.group.id == '164d48fb-2343-332d-b566-1a4884a992e4'


def test_should_get_group_details():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_group_document/get_group_details.yaml'):
        doc = create_group_document(session)

        assert doc.group.name == 'Basket weaving'
