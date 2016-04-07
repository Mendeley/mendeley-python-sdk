import pytest

from mendeley.exception import MendeleyApiException
from test import cassette
from test.resources.documents import *


def test_should_trash_document():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/trash/move_to_trash/trash_document.yaml'), \
            pytest.raises(MendeleyApiException) as ex_info:
        doc = create_document(session)
        doc.move_to_trash()

        session.documents.get(doc.id)

    ex = ex_info.value
    assert ex.status == 404
    assert ex.message == 'Document not found'
