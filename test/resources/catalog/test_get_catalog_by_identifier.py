import pytest
from mendeley.exception import MendeleyException
from test import get_client_credentials_session, cassette
from test.resources.catalog import assert_core_view, assert_bib_view, assert_client_view, assert_stats_view


def test_should_get_by_doi():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_identifier/get_by_doi.yaml'):
        doc = session.catalog.by_identifier(doi='10.1371/journal.pone.0000908')

        assert_core_view(doc)


def test_should_get_by_doi_all_view():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_identifier/get_by_doi_all_view.yaml'):
        doc = session.catalog.by_identifier(doi='10.1371/journal.pone.0000908', view='all')

        assert_core_view(doc)
        assert_bib_view(doc)
        assert_client_view(doc)
        assert_stats_view(doc)


def test_should_get_by_scopus():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_identifier/get_by_scopus.yaml'):
        doc = session.catalog.by_identifier(scopus='2-s2.0-41249100408')

        assert_core_view(doc)


def test_should_raise_if_no_identifier():
    session = get_client_credentials_session()

    with pytest.raises(MendeleyException) as ex_info:
        _ = session.catalog.by_identifier(view='all')

    ex = ex_info.value
    assert str(ex) == 'Must specify exactly one identifier'


def test_should_raise_if_multiple_identifiers():
    session = get_client_credentials_session()

    with pytest.raises(MendeleyException) as ex_info:
        _ = session.catalog.by_identifier(doi='10.1371/journal.pone.0000908', scopus='2-s2.0-41249100408')

    ex = ex_info.value
    assert str(ex) == 'Must specify exactly one identifier'


def test_should_raise_if_not_found():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_identifier/not_found.yaml'), \
            pytest.raises(MendeleyException) as ex_info:
        _ = session.catalog.by_identifier(doi='dodgy-doi')

    ex = ex_info.value
    assert str(ex) == 'Catalog document not found'