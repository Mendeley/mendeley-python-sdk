import json

from oauthlib.oauth2 import MobileApplicationClient, BackendApplicationClient, WebApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from future.builtins import bytes

from mendeley.session import MendeleySession


def handle_text_response(rsp):
    if rsp.headers['content-type'] == 'text/plain':
        rsp._content = bytes(json.dumps({'error': 'invalid_client', 'error_description': rsp.text}), rsp.encoding)
        rsp.headers['content-type'] = 'application/json'

    return rsp


class MendeleyClientCredentialsAuthenticator(object):
    def __init__(self, mendeley):
        self.mendeley = mendeley
        self.client = BackendApplicationClient(mendeley.client_id)

        self.token_url = self.mendeley.host + '/oauth/token'
        self.auth = HTTPBasicAuth(self.mendeley.client_id, self.mendeley.client_secret)

    def authenticate(self):
        oauth = OAuth2Session(client=self.client, scope=['all'])
        oauth.compliance_hook['access_token_response'] = [handle_text_response]

        token = oauth.fetch_token(self.token_url, auth=self.auth, scope=['all'])
        return MendeleySession(self.mendeley,
                               token,
                               client=self.client,
                               refresher=MendeleyClientCredentialsTokenRefresher(self))


class MendeleyLoginAuthenticator:
    def __init__(self, mendeley, client, state):
        self.mendeley = mendeley
        self.client = client
        self.state = state

        self.oauth = OAuth2Session(
            client=client,
            redirect_uri=mendeley.redirect_uri,
            scope=['all'],
            state=state)
        self.oauth.compliance_hook['access_token_response'] = [handle_text_response]

    def get_login_url(self):
        base_url = self.mendeley.host + '/oauth/authorize'
        (login_url, state) = self.oauth.authorization_url(base_url)
        return login_url


class MendeleyAuthorizationCodeAuthenticator(MendeleyLoginAuthenticator):
    def __init__(self, mendeley, state):
        MendeleyLoginAuthenticator.__init__(self, mendeley, WebApplicationClient(mendeley.client_id), state)

        self.token_url = self.mendeley.host + '/oauth/token'
        self.auth = HTTPBasicAuth(self.mendeley.client_id, self.mendeley.client_secret)

    def authenticate(self, redirect_url):
        token = self.oauth.fetch_token(self.token_url,
                                       authorization_response=redirect_url,
                                       auth=self.auth,
                                       scope=['all'])

        return MendeleySession(self.mendeley,
                               token,
                               client=self.client,
                               refresher=MendeleyAuthorizationCodeTokenRefresher(self))


class MendeleyImplicitGrantAuthenticator(MendeleyLoginAuthenticator):
    def __init__(self, mendeley, state):
        client = MobileApplicationClient(mendeley.client_id)
        MendeleyLoginAuthenticator.__init__(self, mendeley, client, state)

    def authenticate(self, redirect_url):
        token = self.oauth.token_from_fragment(redirect_url)
        return MendeleySession(self.mendeley, token, client=self.client)


class MendeleyClientCredentialsTokenRefresher():
    def __init__(self, authenticator):
        self.client = authenticator.client
        self.token_url = authenticator.token_url
        self.auth = authenticator.auth

    def refresh(self, session):
        oauth = OAuth2Session(client=self.client, scope=['all'])
        oauth.compliance_hook['access_token_response'] = [handle_text_response]

        session.token = oauth.fetch_token(self.token_url, auth=self.auth, scope=['all'])


class MendeleyAuthorizationCodeTokenRefresher():
    def __init__(self, authenticator):
        self.client = authenticator.client
        self.token_url = authenticator.token_url
        self.auth = authenticator.auth
        self.redirect_uri = authenticator.mendeley.redirect_uri

    def refresh(self, session):
        oauth = OAuth2Session(client=self.client, redirect_uri=self.redirect_uri, scope=['all'])
        oauth.compliance_hook['access_token_response'] = [handle_text_response]

        session.token = oauth.refresh_token(self.token_url, auth=self.auth, refresh_token=session.token.get('refresh_token', None))
