from itertools import islice
from mendeley.models.common import Position, BoundingBox, Color

from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


def test_should_iterate_through_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/annotations/iter_annotations/iterate_through_annotations.yaml'):
        doc = create_document(session)

        file = doc.attach_file('fixtures/resources/files/basket.txt')

        top_left = Position.create(100, 200)
        bottom_right = Position.create(400, 500)
        bounding_box = BoundingBox.create(top_left, bottom_right, 1)
        color = Color.create(255, 125, 240)

        file.add_sticky_note("annotation 1", 100, 200, 1)
        doc.add_note("annotation 2")
        file.add_sticky_note("annotation 3", 100, 200, 1)
        file.add_highlight([bounding_box], color)

        annotations = list(session.annotations.iter(page_size=2))

        assert len(annotations) == 4
        assert not annotations[0].text
        assert annotations[1].text == 'annotation 3'
        assert annotations[2].text == 'annotation 1'
        assert annotations[3].text == 'annotation 2'
