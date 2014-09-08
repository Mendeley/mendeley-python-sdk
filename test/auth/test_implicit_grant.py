from mendeley import Mendeley
from test import DummyStateGenerator


def test_should_get_implicit_grant_login_url():
    mendeley = Mendeley('id', 'secret', 'https://example.com', state_generator=DummyStateGenerator())
    auth = mendeley.start_implicit_grant_flow()

    assert auth.get_login_url() == 'https://api.mendeley.com/oauth/authorize?' \
                                   'response_type=token&' \
                                   'client_id=id&' \
                                   'redirect_uri=https%3A%2F%2Fexample.com&' \
                                   'scope=all&' \
                                   'state=state1234'


def test_should_get_authenticated_session():
    mendeley = Mendeley('id', 'secret', 'https://example.com', state_generator=DummyStateGenerator())
    auth = mendeley.start_implicit_grant_flow()

    session = auth.authenticate('https://example.com#state=state1234&access_token=token5678&token_type=bearer')

    assert session.token['access_token'] == 'token5678'
    assert session.host == 'https://api.mendeley.com'
