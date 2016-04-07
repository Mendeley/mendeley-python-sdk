from itertools import islice

from test import get_user_session, cassette
from test.resources.documents import create_group_document, delete_all_group_documents


def test_should_iterate_through_group_documents():
    session = get_user_session()
    delete_all_group_documents()

    with cassette('fixtures/resources/documents/iter_group_documents/iterate_through_documents.yaml'):
        create_group_document(session, 'title 1')
        create_group_document(session, 'title 2')
        create_group_document(session, 'title 3')

        docs = list(islice(session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').documents.iter(page_size=2), 3))

        assert len(docs) == 3
        assert docs[0].title == 'title 1'
        assert docs[0].group.name == 'Basket weaving'

        assert docs[1].title == 'title 2'
        assert docs[1].group.name == 'Basket weaving'

        assert docs[2].title == 'title 3'
        assert docs[2].group.name == 'Basket weaving'
