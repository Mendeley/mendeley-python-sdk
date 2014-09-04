from itertools import islice

from test import cassette
from test.resources.documents import *
from test.resources.files import assert_basket_file, assert_weaving_file


def test_should_iterate_through_files():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/iter_files/iterate_through_files.yaml'):
        doc1 = create_document(session)
        doc2 = create_document(session)

        doc1.attach_file('fixtures/resources/files/basket.txt')
        doc1.attach_file('fixtures/resources/files/weaving.txt')
        doc2.attach_file('fixtures/resources/files/basket.txt')

        files = list(islice(session.files.iter(page_size=2), 3))

        assert len(files) == 3
        assert_basket_file(files[0])
        assert_weaving_file(files[1])
        assert_basket_file(files[2])
