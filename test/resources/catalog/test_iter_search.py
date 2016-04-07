from test import get_client_credentials_session, cassette
from itertools import islice


def test_should_iterate_through_search_results():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/iter_search/iterate_through_search_results.yaml'):
        docs = list(islice(session.catalog.search('mapreduce').iter(page_size=2), 3))
        
        # Data in the catalog can change over time so cannot search for exact strings
        # instead search for the keywords we are really interested in
        expected_substring = u'mapreduce'
        assert expected_substring in str(docs[0].title).lower()
        assert expected_substring in str(docs[1].title).lower()
        assert expected_substring in str(docs[2].title).lower()

