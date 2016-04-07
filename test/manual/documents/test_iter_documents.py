from itertools import islice

from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


def test_should_iterate_through_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/iter_documents/iterate_through_documents.yaml'):
        create_document(session, 'title 1')
        create_document(session, 'title 2')
        create_document(session, 'title 3')

        docs = list(islice(session.documents.iter(page_size=2), 3))

        assert len(docs) == 3
        assert docs[0].title == 'title 1'
        assert docs[1].title == 'title 2'
        assert docs[2].title == 'title 3'
