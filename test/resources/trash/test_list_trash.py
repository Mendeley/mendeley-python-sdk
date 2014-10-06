from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


def test_should_page_through_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/list_trash/page_through_documents.yaml'):
        doc1 = create_document(session, 'title 1')
        doc1.move_to_trash()

        doc2 = create_document(session, 'title 2')
        doc2.move_to_trash()

        doc3 = create_document(session, 'title 3')
        doc3.move_to_trash()

        first_page = session.trash.list(page_size=2)
        assert len(first_page.items) == 2
        assert first_page.count == 3

        assert first_page.items[0].title == 'title 1'
        assert first_page.items[1].title == 'title 2'

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 3

        assert second_page.items[0].title == 'title 3'
