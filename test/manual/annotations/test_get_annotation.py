from mendeley.models.common import Position, BoundingBox, Color
from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


def test_should_get_note():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/get_annotation/get_note.yaml'):
        doc = create_document(session)
        annotation = doc.add_note("Initial annotation")

        returned_annotation = session.annotations.get(annotation.id)

        assert returned_annotation.id == annotation.id
        assert returned_annotation.privacy_level == 'private'
        assert returned_annotation.type == 'note'
        assert returned_annotation.last_modified
        assert returned_annotation.profile.id
        assert returned_annotation.profile.display_name
        assert returned_annotation.document().id == doc.id
        assert returned_annotation.document().title == doc.title


def test_should_get_sticky_note():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/get_annotation/get_sticky_note.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')
        annotation = file.add_sticky_note("A nice sticky note", 100, 200, 1)

        returned_annotation = session.annotations.get(annotation.id)

        assert returned_annotation.text == "A nice sticky note"
        assert returned_annotation.privacy_level == 'private'
        assert returned_annotation.type == 'sticky_note'
        assert returned_annotation.last_modified
        assert returned_annotation.profile.id
        assert returned_annotation.profile.display_name
        assert returned_annotation.document().id == doc.id
        assert returned_annotation.document().title == doc.title
        assert returned_annotation.positions[0].top_left.x == 100
        assert returned_annotation.positions[0].top_left.y == 200
        assert returned_annotation.positions[0].bottom_right.x == 100
        assert returned_annotation.positions[0].bottom_right.y == 200
        assert returned_annotation.positions[0].page == 1


def test_should_get_highlight():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/get_annotation/get_highlight.yaml'):

        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        top_left = Position.create(100, 200)
        bottom_right = Position.create(400, 500)
        bounding_box = BoundingBox.create(top_left, bottom_right, 1)
        color = Color.create(255, 125, 240)

        annotation = file.add_highlight([bounding_box], color)

        returned_annotation = session.annotations.get(annotation.id)

        assert not returned_annotation.text
        assert returned_annotation.privacy_level == 'private'
        assert returned_annotation.type == 'highlight'
        assert returned_annotation.last_modified
        assert returned_annotation.profile.id
        assert returned_annotation.profile.display_name
        assert returned_annotation.document().id == doc.id
        assert returned_annotation.document().title == doc.title
        assert returned_annotation.positions[0].top_left.x == 100
        assert returned_annotation.positions[0].top_left.y == 200
        assert returned_annotation.positions[0].bottom_right.x == 400
        assert returned_annotation.positions[0].bottom_right.y == 500
        assert returned_annotation.positions[0].page == 1
        assert returned_annotation.color.r == 255
        assert returned_annotation.color.g == 125
        assert returned_annotation.color.b == 240