from test import cassette
from test.resources.documents import *


def test_should_download_file(tmpdir):
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/download_file/download_file.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')
        downloaded_file = file.download(str(tmpdir))

    with open('fixtures/resources/files/basket.txt') as f1, open(downloaded_file) as f2:
        assert f1.read() == f2.read()
