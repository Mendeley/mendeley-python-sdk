from test import get_user_session, cassette, sleep
from test.resources.documents import create_document, assert_core_document, delete_all_documents, assert_bib_document


def test_should_list_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/list_documents.yaml'):
        create_document(session)

        page = session.documents.list()
        assert len(page.items) == 1
        assert page.count == 1

        assert_core_document(page.items[0])


def test_should_page_through_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/page_through_documents.yaml'):
        create_document(session, 'title 1')
        create_document(session, 'title 2')
        create_document(session, 'title 3')

        first_page = session.documents.list(page_size=2)
        assert len(first_page.items) == 2
        assert first_page.count == 3

        assert first_page.items[0].title == 'title 1'
        assert first_page.items[1].title == 'title 2'

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 3

        assert second_page.items[0].title == 'title 3'


def test_should_sort_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/sort_documents.yaml'):
        create_document(session, 'B title 1')
        create_document(session, 'A title 2')
        create_document(session, 'C title 3')

        page = session.documents.list(sort='title')
        assert len(page.items) == 3
        assert page.count == 3

        assert page.items[0].title == 'A title 2'
        assert page.items[1].title == 'B title 1'
        assert page.items[2].title == 'C title 3'


def test_should_sort_documents_desc():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/sort_documents_desc.yaml'):
        create_document(session, 'B title 1')
        create_document(session, 'A title 2')
        create_document(session, 'C title 3')

        page = session.documents.list(sort='title', order='desc')
        assert len(page.items) == 3
        assert page.count == 3

        assert page.items[0].title == 'C title 3'
        assert page.items[1].title == 'B title 1'
        assert page.items[2].title == 'A title 2'


def test_should_list_documents_modified_since():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/modified_since.yaml'):
        doc1 = create_document(session, 'title 1')
        sleep(2)

        create_document(session, 'title 2')
        create_document(session, 'title 3')

        page = session.documents.list(modified_since=doc1.created.replace(seconds=+1))
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].title == 'title 2'
        assert page.items[1].title == 'title 3'


def test_should_list_documents_deleted_since():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/deleted_since.yaml'):
        doc1 = create_document(session, 'title 1')
        doc2 = create_document(session, 'title 2')
        doc3 = create_document(session, 'title 3')

        doc1.delete()
        sleep(2)

        doc2.delete()
        doc3.delete()

        page = session.documents.list(deleted_since=doc3.created.replace(seconds=+1))
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].id == doc2.id
        assert page.items[1].id == doc3.id


def test_should_list_with_bib_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_documents/bib_view.yaml'):
        create_document(session)

        page = session.documents.list(view='bib')
        assert len(page.items) == 1
        assert page.count == 1

        assert_core_document(page.items[0])
        assert_bib_document(page.items[0])
