from mendeley.models.common import BoundingBox, Position, Color
from test import get_user_session, cassette
from test.resources.documents import create_document


def test_should_add_note():
    session = get_user_session()

    with cassette('fixtures/resources/annotations/add_annotation/add_note.yaml'):
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


def test_should_add_sticky_note():
    session = get_user_session()

    with cassette('fixtures/resources/annotations/add_annotation/add_sticky_note.yaml'):

        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        annotation = file.add_sticky_note("A nice sticky note", 100, 200, 1)

        assert annotation.text == "A nice sticky note"
        assert annotation.privacy_level == 'private'
        assert annotation.type == 'sticky_note'
        assert annotation.last_modified
        assert annotation.profile.id
        assert annotation.profile.display_name
        assert annotation.document().id == doc.id
        assert annotation.document().title == doc.title
        assert annotation.positions[0].top_left.x == 100
        assert annotation.positions[0].top_left.y == 200
        assert annotation.positions[0].bottom_right.x == 100
        assert annotation.positions[0].bottom_right.y == 200
        assert annotation.positions[0].page == 1


def test_should_add_highlight():
    session = get_user_session()

    with cassette('fixtures/resources/annotations/add_annotation/add_highlight.yaml'):

        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        top_left = Position.create(100, 200)
        bottom_right = Position.create(400, 500)
        bounding_box = BoundingBox.create(top_left, bottom_right, 1)
        color = Color.create(255, 125, 240)

        annotation = file.add_highlight([bounding_box], color)

        assert not annotation.text
        assert annotation.privacy_level == 'private'
        assert annotation.type == 'highlight'
        assert annotation.last_modified
        assert annotation.profile.id
        assert annotation.profile.display_name
        assert annotation.document().id == doc.id
        assert annotation.document().title == doc.title
        assert annotation.positions[0].top_left.x == 100
        assert annotation.positions[0].top_left.y == 200
        assert annotation.positions[0].bottom_right.x == 400
        assert annotation.positions[0].bottom_right.y == 500
        assert annotation.positions[0].page == 1
        assert annotation.color.r == 255
        assert annotation.color.g == 125
        assert annotation.color.b == 240