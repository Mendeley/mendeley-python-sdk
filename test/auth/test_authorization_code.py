from mendeley import Mendeley
from test import configure_mendeley, cassette, DummyStateGenerator


def test_should_get_auth_code_login_url():
    mendeley = Mendeley('id', 'secret', 'https://example.com', state_generator=DummyStateGenerator())
    auth = mendeley.start_authorization_code_flow()

    assert auth.get_login_url() == 'https://api.mendeley.com/oauth/authorize?' \
                                   'response_type=code&' \
                                   'client_id=id&' \
                                   'redirect_uri=https%3A%2F%2Fexample.com&' \
                                   'scope=all&' \
                                   'state=state1234'


def test_should_get_authenticated_session():
    mendeley = configure_mendeley()
    auth = mendeley.start_authorization_code_flow()

    with cassette('fixtures/auth/authorization_code/get_authenticated_session.yaml'):
        session = auth.authenticate('https://example.com?state=state1234&code=VE1PtGf81OnTA97S545_9a7GWCA')

        assert session.token['access_token']
        assert session.host == 'https://api.mendeley.com'
