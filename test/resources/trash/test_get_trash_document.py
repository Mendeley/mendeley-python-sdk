from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document, assert_core_document, assert_bib_document, \
    assert_client_document, assert_tags_document, assert_all_document


def test_should_get_document_core_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/get_document/get_document_core_view.yaml'):
        created_doc = create_document(session)
        created_doc.move_to_trash()

        doc = session.trash.get(created_doc.id)
        assert_core_document(doc)


def test_should_get_document_bib_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/get_document/get_document_bib_view.yaml'):
        created_doc = create_document(session)
        created_doc.move_to_trash()

        doc = session.trash.get(created_doc.id, view='bib')
        assert_core_document(doc)
        assert_bib_document(doc)


def test_should_get_document_client_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/get_document/get_document_client_view.yaml'):
        created_doc = create_document(session)
        created_doc.move_to_trash()

        doc = session.trash.get(created_doc.id, view='client')
        assert_core_document(doc)
        assert_client_document(doc)


def test_should_get_document_tags_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/get_document/get_document_tags_view.yaml'):
        created_doc = create_document(session)
        created_doc.move_to_trash()

        doc = session.trash.get(created_doc.id, view='tags')
        assert_core_document(doc)
        assert_tags_document(doc)


def test_should_get_document_all_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/get_document/get_document_all_view.yaml'):
        created_doc = create_document(session)
        created_doc.move_to_trash()

        doc = session.trash.get(created_doc.id, view='all')
        assert_all_document(doc)


def test_should_be_able_to_get_profile_for_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/get_document/get_profile_for_document.yaml'):
        created_doc = create_document(session)
        created_doc.move_to_trash()

        doc = session.trash.get(created_doc.id)
        profile = session.profiles.me

        assert doc.profile.display_name == profile.display_name
