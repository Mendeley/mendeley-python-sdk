from itertools import islice
import sys

import pytest

from test import get_user_session, cassette
from test.resources.documents import delete_all_documents, create_document


@pytest.mark.xfail(sys.version_info[0] == 3, reason='vcrpy issue #96')
def test_should_iterate_through_documents():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/iter_trash/iterate_through_documents.yaml'):
        doc1 = create_document(session, 'title 1')
        doc1.move_to_trash()

        doc2 = create_document(session, 'title 2')
        doc2.move_to_trash()

        doc3 = create_document(session, 'title 3')
        doc3.move_to_trash()

        docs = list(islice(session.trash.iter(page_size=2), 3))

        assert len(docs) == 3
        assert docs[0].title == 'title 1'
        assert docs[1].title == 'title 2'
        assert docs[2].title == 'title 3'
