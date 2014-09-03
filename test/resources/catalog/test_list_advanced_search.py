from test import get_client_credentials_session, cassette


def test_should_page_through_search_results():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/list_advanced_search/page_through_search_results.yaml'):
        search = session.catalog.advanced_search(title='mapreduce', author='Jeffrey Dean')
        first_page = search.list(page_size=2)

        assert len(first_page.items) == 2
        assert first_page.count == 173631

        assert first_page.items[0].title == 'Experiences with MapReduce, an abstraction for large-scale computation'
        assert first_page.items[1].title == 'MapReduce'

        second_page = first_page.next_page

        assert len(second_page.items) == 2
        assert second_page.count == 173631

        assert second_page.items[0].title == 'MapReduce map & reduce function for large datasets'
        assert second_page.items[1].title == 'MapReduce: SimplifiedDataProcessing onLargeClusters'


def test_should_list_search_results_all_view():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/list_advanced_search/list_search_results_all_view.yaml'):
        first_page = session.catalog.advanced_search(title='mapreduce', author='Jeffrey Dean', view='all') \
            .list(page_size=2)

        assert len(first_page.items) == 2
        assert first_page.count == 173631

        assert first_page.items[0].title == 'Experiences with MapReduce, an abstraction for large-scale computation'
        assert first_page.items[0].reader_count == 55
