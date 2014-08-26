from oauthlib.oauth2 import InvalidClientError
import pytest

from test import configure_mendeley, cassette


def test_should_get_authenticated_session():
    mendeley = configure_mendeley()
    auth = mendeley.start_client_credentials_flow()

    with cassette('fixtures/auth/client_credentials/get_authenticated_session.yaml'):
        session = auth.authenticate()

    assert session.token['access_token']
    assert session.mendeley.host == 'https://api.mendeley.com'


def test_should_throw_exception_on_incorrect_credentials():
    mendeley = configure_mendeley()
    mendeley.client_secret += '-invalid'
    auth = mendeley.start_client_credentials_flow()

    with cassette('fixtures/auth/client_credentials/incorrect_credentials.yaml'), pytest.raises(InvalidClientError):
        auth.authenticate()
