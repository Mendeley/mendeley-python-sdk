import random
import string
import json

from oauthlib.oauth2 import MobileApplicationClient, BackendApplicationClient, WebApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from future.builtins import bytes

from mendeley.session import MendeleySession


class DefaultStateGenerator(object):
    ASCII_CHARACTER_SET = string.ascii_uppercase + string.digits

    @staticmethod
    def generate_state(length=30, chars=ASCII_CHARACTER_SET):
        rand = random.SystemRandom()
        return ''.join(rand.choice(chars) for _ in range(length))


def handle_text_response(rsp):
    if rsp.headers['content-type'] == 'text/plain':
        rsp._content = bytes(json.dumps({'error': 'invalid_client', 'error_description': rsp.text}), rsp.encoding)
        rsp.headers['content-type'] = 'application/json'

    return rsp


class MendeleyClientCredentialsAuthenticator(object):
    def __init__(self, mendeley):
        self.mendeley = mendeley

        self.oauth = OAuth2Session(
            client=BackendApplicationClient(mendeley.client_id),
            scope=['all'])
        self.oauth.compliance_hook['access_token_response'] = [handle_text_response]

    def authenticate(self):
        token_url = self.mendeley.host + '/oauth/token'
        auth = HTTPBasicAuth(self.mendeley.client_id, self.mendeley.client_secret)

        token = self.oauth.fetch_token(token_url, auth=auth, scope=['all'])
        return MendeleySession(self.mendeley, token['access_token'], expires_in=token.get('expires_in'))


class MendeleyLoginAuthenticator:
    def __init__(self, mendeley, client, state_generator=None):
        self.mendeley = mendeley

        state_generator = state_generator or DefaultStateGenerator()
        self.state = state_generator.generate_state()

        self.oauth = OAuth2Session(
            client=client,
            redirect_uri=mendeley.redirect_uri,
            scope=['all'],
            state=self.state)
        self.oauth.compliance_hook['access_token_response'] = [handle_text_response]

    def get_login_url(self):
        base_url = self.mendeley.host + '/oauth/authorize'
        (login_url, state) = self.oauth.authorization_url(base_url)
        return login_url


class MendeleyAuthorizationCodeAuthenticator(MendeleyLoginAuthenticator):
    def __init__(self, mendeley, state_generator=None):
        client = WebApplicationClient(mendeley.client_id)
        MendeleyLoginAuthenticator.__init__(self, mendeley, client, state_generator)

    def authenticate(self, redirect_url):
        token_url = self.mendeley.host + '/oauth/token'
        auth = HTTPBasicAuth(self.mendeley.client_id, self.mendeley.client_secret)

        token = self.oauth.fetch_token(token_url, authorization_response=redirect_url, auth=auth, scope=['all'])
        return MendeleySession(self.mendeley, token['access_token'], expires_in=token.get('expires_in'))


class MendeleyImplicitGrantAuthenticator(MendeleyLoginAuthenticator):
    def __init__(self, mendeley, state_generator=None):
        client = MobileApplicationClient(mendeley.client_id)
        MendeleyLoginAuthenticator.__init__(self, mendeley, client, state_generator)

    def authenticate(self, redirect_url):
        token = self.oauth.token_from_fragment(redirect_url)
        return MendeleySession(self.mendeley, token['access_token'], expires_in=token.get('expires_in'))
