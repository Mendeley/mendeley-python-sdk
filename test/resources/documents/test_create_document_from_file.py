from test import cassette
from test.resources.documents import *


def test_should_create_document_from_file():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/create_document_from_file/create_document_from_file.yaml'):
        doc = session.documents.create_from_file('fixtures/resources/files/basket.txt')

        assert doc.id
        assert doc.title == 'basket.txt'
        assert doc.type == 'journal'
