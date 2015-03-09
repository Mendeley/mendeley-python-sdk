from test import get_user_session, cassette, sleep
from test.resources.documents import create_document, assert_core_document, delete_all_documents, assert_bib_document


def test_should_list_annotations():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/list_annotations/list_annotations.yaml'):
        doc = create_document(session)

        doc.add_note("A nice annotation")

        page = session.annotations.list()
        assert len(page.items) == 1
        assert page.count == 1

        annotation = page.items[0]

        assert annotation.text == "A nice annotation"
        assert annotation.privacy_level == 'private'
        assert annotation.type == 'note'
        assert annotation.last_modified
        assert annotation.profile.id
        assert annotation.profile.display_name
        assert annotation.document().id == doc.id
        assert annotation.document().title == doc.title


def test_should_page_through_annotations():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/list_annotations/page_through_annotations.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        file.add_sticky_note("annotation 1", 100, 200, 1)
        file.add_sticky_note("annotation 2", 100, 200, 1)
        file.add_sticky_note("annotation 3", 100, 200, 1)

        first_page = session.annotations.list(page_size=2)
        assert len(first_page.items) == 2
        assert first_page.count == 3

        assert first_page.items[0].text == 'annotation 2'
        assert first_page.items[1].text == 'annotation 1'

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 3

        assert second_page.items[0].text == 'annotation 3'


def test_should_list_annotations_modified_since():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/list_annotations/modified_since.yaml'):
        doc = create_document(session, 'title 1')
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        annotation = file.add_sticky_note("annotation 1", 100, 200, 1)
        sleep(2)

        file.add_sticky_note("annotation 2", 100, 200, 1)
        file.add_sticky_note("annotation 3", 100, 200, 1)

        page = session.annotations.list(modified_since=annotation.created.replace(seconds=+1))
        assert len(page.items) == 2
        assert page.count == 2

        assert page.items[0].text == 'annotation 2'
        assert page.items[1].text == 'annotation 3'


def test_should_list_annotations_deleted_since():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/list_annotations/deleted_since.yaml'):
        doc = create_document(session, 'title 1')
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        annotation1 = file.add_sticky_note("annotation 1", 100, 200, 1)
        annotation2 = file.add_sticky_note("annotation 2", 100, 200, 1)
        annotation3 = file.add_sticky_note("annotation 3", 100, 200, 1)


        annotation1.delete()
        sleep(2)

        annotation2.delete()
        annotation3.delete()

        page = session.annotations.list(deleted_since=annotation3.created.replace(seconds=+1))
        assert len(page.items) == 2
        assert page.count == 2