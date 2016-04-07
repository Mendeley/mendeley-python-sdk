import pytest
from mendeley.exception import MendeleyApiException
from test import get_client_credentials_session, cassette
from test.resources.catalog import assert_core_view, assert_all_view


def test_should_lookup_by_metadata():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/lookup/lookup_by_metadata.yaml'):
        doc = session.catalog.lookup(
            title='Changes in tree reproductive traits reduce functional diversity in a fragmented '
                  'Atlantic forest landscape',
            year=2007,
            source='PLoS ONE'
        )

        assert doc.score == 91
        assert_core_view(doc)


def test_should_lookup_by_metadata_all_view():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/lookup/lookup_by_metadata_all_view.yaml'):
        doc = session.catalog.lookup(
            title='Changes in tree reproductive traits reduce functional diversity in a fragmented '
                  'Atlantic forest landscape',
            year=2007,
            source='PLoS ONE',
            view='all'
        )

        assert doc.score == 91
        assert_all_view(doc)


def test_should_lookup_by_doi():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/lookup/lookup_by_doi.yaml'):
        doc = session.catalog.lookup(doi='10.1371/journal.pone.0000908')

        assert doc.score == 100
        assert_core_view(doc)


def test_should_raise_on_not_found():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/lookup/not_found.yaml'), \
         pytest.raises(MendeleyApiException) as ex_info:
        doc = session.catalog.lookup(
            title='Underwater basket weaving',
            authors='Piers Bursill-Hall'
        )

        assert doc.score == 91
        assert_core_view(doc)

    ex = ex_info.value
    assert ex.status == 404
