from test import get_user_session, cassette
from test.resources.documents import create_document, delete_all_documents


def test_should_delete_annotation():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/delete_annotation/delete_annotation.yaml'):
        doc = create_document(session)
        annotation = doc.add_note("A nice annotation")

        annotation.delete()

        page = session.annotations.list()
        assert not page.items