from mendeley.auth import MendeleyClientCredentialsAuthenticator, \
    MendeleyAuthorizationCodeAuthenticator, \
    MendeleyImplicitGrantAuthenticator


class Mendeley(object):
    def __init__(self, client_id, client_secret=None, redirect_uri=None, host='https://api.mendeley.com'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.host = host

    def start_client_credentials_flow(self):
        return MendeleyClientCredentialsAuthenticator(self)

    def start_authorization_code_flow(self, state_generator=None):
        return MendeleyAuthorizationCodeAuthenticator(self, state_generator)

    def start_implicit_grant_flow(self, state_generator=None):
        return MendeleyImplicitGrantAuthenticator(self, state_generator)
