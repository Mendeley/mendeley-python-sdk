from test import get_client_credentials_session, cassette
from itertools import islice


def test_should_iterate_through_search_results():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/iter_search/iterate_through_search_results.yaml'):
        docs = list(islice(session.catalog.search('mapreduce').iter(page_size=2), 3))

        assert docs[0].title == 'Rapid parallel genome indexing with MapReduce'
        assert docs[1].title == 'MapReduce'
        assert docs[2].title == 'Mumak: Map-Reduce Simulator'

