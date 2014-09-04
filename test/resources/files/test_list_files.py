from test import cassette, sleep
from test.resources.documents import *
from test.resources.files import assert_basket_file, assert_weaving_file


def test_should_list_files():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/list_files/list_files.yaml'):
        doc = create_document(session)
        doc.attach_file('fixtures/resources/files/basket.txt')

        page = session.files.list()
        assert len(page.items) == 1
        assert page.count == 1

        assert_basket_file(page.items[0])


def test_should_page_through_files():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/list_files/page_through_files.yaml'):
        doc1 = create_document(session)
        doc2 = create_document(session)

        doc1.attach_file('fixtures/resources/files/basket.txt')
        doc1.attach_file('fixtures/resources/files/weaving.txt')
        doc2.attach_file('fixtures/resources/files/basket.txt')

        first_page = session.files.list(page_size=2)
        assert len(first_page.items) == 2
        assert first_page.count == 3

        assert_basket_file(first_page.items[0])
        assert_weaving_file(first_page.items[1])

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 3
        assert_basket_file(second_page.items[0])


def test_should_list_files_by_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/list_files/list_files_by_document.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        page = doc.files.list()
        assert len(page.items) == 1
        assert page.count == 1

        assert_basket_file(file)


def test_should_list_files_by_group():
    session = get_user_session()
    delete_all_group_documents()

    with cassette('fixtures/resources/files/list_files/list_files_by_group.yaml'):
        doc = create_group_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        page = session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').files.list()
        assert len(page.items) == 1
        assert page.count == 1

        assert_basket_file(file)


def test_should_list_files_added_since():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/list_files/added_since.yaml'):
        doc1 = create_document(session)
        doc1.attach_file('fixtures/resources/files/basket.txt')

        sleep(2)

        doc2 = create_document(session)
        doc2.attach_file('fixtures/resources/files/basket.txt')
        doc2.attach_file('fixtures/resources/files/weaving.txt')

        page = session.files.list(added_since=doc2.created.replace(seconds=-1))
        assert len(page.items) == 2
        assert page.count == 2

        assert_basket_file(page.items[0])
        assert_weaving_file(page.items[1])


def test_should_list_files_deleted_since():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/list_files/deleted_since.yaml'):
        doc = create_document(session)
        file1 = doc.attach_file('fixtures/resources/files/basket.txt')
        file2 = doc.attach_file('fixtures/resources/files/weaving.txt')

        sleep(1)

        file1.delete()
        file2.delete()

        page = session.files.list(deleted_since=doc.created)
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].id == file1.id
        assert page.items[1].id == file2.id


def test_should_get_document_for_file():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/files/list_files/get_document_for_file.yaml'):
        doc = create_document(session)
        doc.attach_file('fixtures/resources/files/basket.txt')

        page = session.files.list()
        assert len(page.items) == 1
        assert page.count == 1

        assert page.items[0].document().title == 'Underwater basket weaving'
