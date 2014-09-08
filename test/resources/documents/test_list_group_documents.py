import sys

import pytest

from test import get_user_session, cassette
from test.resources.documents import delete_all_group_documents, create_group_document


@pytest.mark.xfail(sys.version_info[0] == 3, reason='vcrpy issue #96')
def test_should_page_through_group_documents():
    session = get_user_session()
    delete_all_group_documents()

    with cassette('fixtures/resources/documents/list_group_documents/page_through_documents.yaml'):
        create_group_document(session, 'title 1')
        create_group_document(session, 'title 2')
        create_group_document(session, 'title 3')

        first_page = session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').documents.list(page_size=2)
        assert len(first_page.items) == 2
        assert first_page.count == 3

        assert first_page.items[0].title == 'title 1'
        assert first_page.items[0].group.name == 'Basket weaving'

        assert first_page.items[1].title == 'title 2'
        assert first_page.items[1].group.name == 'Basket weaving'

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 3

        assert second_page.items[0].title == 'title 3'
        assert second_page.items[0].group.name == 'Basket weaving'