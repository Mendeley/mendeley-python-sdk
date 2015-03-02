from test import get_user_session, cassette
from test.resources.documents import create_document


def test_should_add_note():
    session = get_user_session()

    with cassette('fixtures/resources/annotations/add_note/add_note.yaml'):
        doc = create_document(session)

        annotation = doc.add_note("A nice annotation")

        assert annotation.text == "A nice annotation"
        assert annotation.privacy_level == 'private'
        assert annotation.type == 'note'
        assert annotation.last_modified
        assert annotation.profile.id
        assert annotation.profile.display_name
        assert annotation.document().id == doc.id
        assert annotation.document().title == doc.title

