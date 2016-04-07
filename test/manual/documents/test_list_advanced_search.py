import pytest
from mendeley.exception import MendeleyException
from test import cassette, sleep
from test.resources.documents import *


def test_should_page_through_search_results():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_advanced_search/page_through_search_results.yaml'):
        session.documents.create('Underwater basket weaving', 'journal', source='Journal of Submarine Bambrology')
        session.documents.create('Underwater bucket weaving', 'journal', source='Journal of Submarine Bucketology')
        session.documents.create('Overground basket weaving', 'journal', source='Journal of Aeronautical Bambrology')
        session.documents.create('Underwater basket knitting', 'journal', source='Journal of Submarine Woolonomics')

        sleep(3)

        first_page = session.documents.advanced_search(title='basket', source='submarine').list(page_size=1)

        assert len(first_page.items) == 1
        assert first_page.count == 2

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 2

        titles = set([doc.title for doc in first_page.items + second_page.items])
        assert titles == {'Underwater basket weaving', 'Underwater basket knitting'}


def test_should_not_be_able_to_search_group_documents():
    session = get_user_session()

    with cassette('fixtures/resources/documents/list_advanced_search/group.yaml'), \
            pytest.raises(MendeleyException) as ex_info:
        _ = session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').documents.advanced_search(title='basket')

    ex = ex_info.value
    assert str(ex) == 'Search is not available for group documents'
