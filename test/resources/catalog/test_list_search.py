from test import get_client_credentials_session, cassette


def test_should_page_through_search_results():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/list_search/page_through_search_results.yaml'):
        first_page = session.catalog.search('mapreduce').list(page_size=2)

        assert len(first_page.items) == 2
        assert first_page.count == 1781

        assert first_page.items[0].title == 'Rapid parallel genome indexing with MapReduce'
        assert first_page.items[1].title == 'MapReduce'

        second_page = first_page.next_page

        assert len(second_page.items) == 2
        assert second_page.count == 1781

        assert second_page.items[0].title == 'Mumak: Map-Reduce Simulator'
        assert second_page.items[1].title == 'Exploring mapreduce efficiency with highly-distributed data'


def test_should_list_search_results_all_view():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/list_search/list_search_results_all_view.yaml'):
        first_page = session.catalog.search('mapreduce', view='all').list(page_size=2)

        assert len(first_page.items) == 2
        assert first_page.count == 1781

        assert first_page.items[0].title == 'Rapid parallel genome indexing with MapReduce'
        assert first_page.items[0].publisher == 'ACM Press'
