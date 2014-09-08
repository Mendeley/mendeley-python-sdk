import os
import random
import string

from future.moves.urllib.parse import urlsplit

from mendeley.auth import MendeleyClientCredentialsAuthenticator, \
    MendeleyAuthorizationCodeAuthenticator, \
    MendeleyImplicitGrantAuthenticator


class Mendeley(object):
    def __init__(self,
                 client_id,
                 client_secret=None,
                 redirect_uri=None,
                 host='https://api.mendeley.com',
                 state_generator=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.host = host
        self.state_generator = state_generator or DefaultStateGenerator()

        if is_localhost(redirect_uri):
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    def start_client_credentials_flow(self):
        return MendeleyClientCredentialsAuthenticator(self)

    def start_authorization_code_flow(self, state=None):
        state = state or self.state_generator.generate_state()
        return MendeleyAuthorizationCodeAuthenticator(self, state)

    def start_implicit_grant_flow(self, state=None):
        state = state or self.state_generator.generate_state()
        return MendeleyImplicitGrantAuthenticator(self, state)


class DefaultStateGenerator(object):
    ASCII_CHARACTER_SET = string.ascii_uppercase + string.digits

    @staticmethod
    def generate_state(length=30, chars=ASCII_CHARACTER_SET):
        rand = random.SystemRandom()
        return ''.join(rand.choice(chars) for _ in range(length))


def is_localhost(url):
    split_url = urlsplit(url)
    return split_url.scheme == 'http' and split_url.hostname in ['127.0.0.1', '0.0.0.0', 'localhost']
