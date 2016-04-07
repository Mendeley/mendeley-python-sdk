from test import cassette
from test.resources.documents import *


def test_should_delete_file():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/delete_file/delete_file.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')
        file.delete()

        assert doc.files.list().count == 0
