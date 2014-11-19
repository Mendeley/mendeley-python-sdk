import pytest

from mendeley.exception import MendeleyException
from test import cassette, sleep
from test.resources.documents import *


def test_should_page_through_search_results():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_search/page_through_search_results.yaml'):
        session.documents.create('Underwater basket weaving', 'journal')
        session.documents.create('Underwater bucket weaving', 'journal')
        session.documents.create('Overground basket weaving', 'journal')
        session.documents.create('Underwater basket knitting', 'journal')

        sleep(3)

        first_page = session.documents.search('basket').list(page_size=2)

        assert len(first_page.items) == 2
        assert first_page.count == 3

        second_page = first_page.next_page
        assert len(second_page.items) == 1
        assert second_page.count == 3

        titles = set([doc.title for doc in first_page.items + second_page.items])
        assert titles == {'Underwater basket weaving', 'Overground basket weaving', 'Underwater basket knitting'}


def test_should_list_search_results_all_view():
    session = get_user_session()
    delete_all_documents()

    with cassette('fixtures/resources/documents/list_search/list_search_results_all_view.yaml'):
        session.documents.create('Underwater basket weaving', 'journal', publisher='ACM Press')

        sleep(3)

        first_page = session.documents.search('basket', view='all').list()

        assert len(first_page.items) == 1
        assert first_page.count == 1
        assert first_page.items[0].publisher == 'ACM Press'


def test_should_not_be_able_to_search_group_documents():
    session = get_user_session()

    with cassette('fixtures/resources/documents/list_search/group.yaml'), \
            pytest.raises(MendeleyException) as ex_info:
        _ = session.groups.get('164d48fb-2343-332d-b566-1a4884a992e4').documents.search('basket')

    ex = ex_info.value
    assert str(ex) == 'Search is not available for group documents'
