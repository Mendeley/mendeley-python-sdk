from itertools import islice

from test import get_user_session, cassette
from test.resources.documents import create_group_document, delete_all_group_documents


def test_should_iterate_through_documents():
    session = get_user_session()
    delete_all_group_documents()

    with cassette('fixtures/resources/trash/iter_group_trash/iterate_through_documents.yaml'):
        doc1 = create_group_document(session, 'title 1')
        doc1.move_to_trash()

        doc2 = create_group_document(session, 'title 2')
        doc2.move_to_trash()

        doc3 = create_group_document(session, 'title 3')
        doc3.move_to_trash()

        docs = list(islice(session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').trash.iter(page_size=2), 3))

        assert len(docs) == 3
        assert docs[0].title == 'title 1'
        assert docs[0].group.name == 'Basket weaving'

        assert docs[1].title == 'title 2'
        assert docs[1].group.name == 'Basket weaving'

        assert docs[2].title == 'title 3'
        assert docs[2].group.name == 'Basket weaving'
