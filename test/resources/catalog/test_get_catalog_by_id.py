import pytest

from mendeley.exception import MendeleyApiException
from test import get_client_credentials_session, cassette
from test.resources.catalog import assert_core_view, assert_bib_view, assert_client_view, assert_stats_view, \
    assert_all_view


def test_should_get_core_view():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_id/get_core_view.yaml'):
        doc = session.catalog.get('5cd8328e-febe-3299-8e26-cf6ab2c07f0f')

        assert_core_view(doc)


def test_should_get_bib_view_by_id():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_id/get_bib_view.yaml'):
        doc = session.catalog.get('5cd8328e-febe-3299-8e26-cf6ab2c07f0f', view='bib')

        assert_core_view(doc)
        assert_bib_view(doc)


def test_should_get_client_view_by_id():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_id/get_client_view.yaml'):
        doc = session.catalog.get('5cd8328e-febe-3299-8e26-cf6ab2c07f0f', view='client')

        assert_core_view(doc)
        assert_client_view(doc)


def test_should_get_stats_view_by_id():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_id/get_stats_view.yaml'):
        doc = session.catalog.get('5cd8328e-febe-3299-8e26-cf6ab2c07f0f', view='stats')

        assert_core_view(doc)
        assert_stats_view(doc)


def test_should_get_all_view_by_id():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_id/get_all_view.yaml'):
        doc = session.catalog.get('5cd8328e-febe-3299-8e26-cf6ab2c07f0f', view='all')

        assert_all_view(doc)


def test_should_throw_on_bad_view():
    session = get_client_credentials_session()

    with cassette('fixtures/resources/catalog/get_catalog_by_id/get_bad_view.yaml'), \
         pytest.raises(MendeleyApiException) as ex_info:
        _ = session.catalog.get('5cd8328e-febe-3299-8e26-cf6ab2c07f0f', view='bad')

    ex = ex_info.value
    assert ex.status == 400
    assert ex.message == 'Invalid view'