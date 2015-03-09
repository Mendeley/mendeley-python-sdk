from mendeley.models.common import Position, BoundingBox, Color
from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


def test_should_update_text_of_a_note():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/update_annotations/update_note.yaml'):
        doc = create_document(session)
        annotation = doc.add_note("Initial annotation")

        patched_annotation = annotation.update(text="New text")

        assert patched_annotation.text == "New text"
        assert annotation.id == patched_annotation.id


def test_should_update_sticky_note():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/update_annotations/update_sticky_note.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')
        annotation = file.add_sticky_note("Initial annotation", 100, 200, 1)

        top_left = Position.create(400, 300)
        bottom_right = Position.create(400, 300)
        bounding_box = BoundingBox.create(top_left, bottom_right, 2)
        patched_annotation = annotation.update(text="New text", positions=[bounding_box])

        assert patched_annotation.text == "New text"
        assert patched_annotation.positions[0].top_left.x == 400
        assert patched_annotation.positions[0].top_left.y == 300
        assert patched_annotation.positions[0].bottom_right.x == 400
        assert patched_annotation.positions[0].bottom_right.y == 300
        assert patched_annotation.positions[0].page == 2
        assert annotation.id == patched_annotation.id



def test_should_update_highlight():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/update_annotations/update_highlight.yaml'):
        doc = create_document(session)
        file = doc.attach_file('fixtures/resources/files/basket.txt')

        top_left = Position.create(400, 300)
        bottom_right = Position.create(400, 300)
        bounding_box = BoundingBox.create(top_left, bottom_right, 2)
        color = Color.create(255, 125, 240)
        updated_color = Color.create(123, 456, 222)

        annotation = file.add_highlight([bounding_box], color)

        patched_annotation = annotation.update(text="New text", positions=[bounding_box], color=updated_color)

        assert patched_annotation.text == "New text"
        assert patched_annotation.positions[0].top_left.x == 400
        assert patched_annotation.positions[0].top_left.y == 300
        assert patched_annotation.positions[0].bottom_right.x == 400
        assert patched_annotation.positions[0].bottom_right.y == 300
        assert patched_annotation.positions[0].page == 2
        assert patched_annotation.color.r == 123
        assert patched_annotation.color.g == 456
        assert patched_annotation.color.b == 222
        assert annotation.id == patched_annotation.id