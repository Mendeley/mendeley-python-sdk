from test import cassette
from test.resources.documents import *


def test_should_upload_file():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/upload_file/upload_file.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        assert file.id
        assert file.size == 178
        assert file.file_name == 'Underwater basket weaving'
        assert file.mime_type == 'text/plain'
        assert file.filehash == '92c7a71b371eb439579be559b5eac9c09a743c42'
