from oauthlib.oauth2 import InvalidClientError
import pytest
import vcr

from test import configure_mendeley


@vcr.use_cassette('fixtures/auth/client_credentials/get_authenticated_session.yaml', filter_headers=['authorization'])
def test_should_get_authenticated_session():
    mendeley = configure_mendeley()
    auth = mendeley.start_client_credentials_flow()

    session = auth.authenticate()

    assert session.token['access_token'] == 'MSwxNDA5MDU0NzAwMTgyLCw4MDEsLCwzWGt1OEV6cEViOEhNck0wVU05ZFp6TmVpbUU'
    assert session.mendeley.host == 'https://api.mendeley.com'


@vcr.use_cassette('fixtures/auth/client_credentials/incorrect_credentials.yaml', filter_headers=['authorization'])
def test_should_throw_exception_on_incorrect_credentials():
    mendeley = configure_mendeley()
    mendeley.client_secret += '-invalid'
    auth = mendeley.start_client_credentials_flow()

    with pytest.raises(InvalidClientError):
        auth.authenticate()
