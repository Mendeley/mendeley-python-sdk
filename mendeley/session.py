from future.moves.urllib.parse import urljoin
from requests_oauthlib import OAuth2Session

from mendeley.exception import MendeleyException
from mendeley.resources import Groups, Profiles


class MendeleySession(OAuth2Session):
    def __init__(self, mendeley, access_token, expires_in=None, refresh_token=None):
        super(MendeleySession, self).__init__(client_id=mendeley.client_id,
                                              token=self.__token_dict(access_token, expires_in, refresh_token))
        self.mendeley = mendeley

        self.profiles = Profiles(self)
        self.groups = Groups(self)

    @staticmethod
    def __token_dict(access_token, expires_in, refresh_token):
        token = {'access_token': access_token}
        if expires_in:
            token['expires_in'] = expires_in
        if refresh_token:
            token['refresh_token'] = refresh_token
        return token

    def request(self, method, url, data=None, headers=None, **kwargs):
        full_url = urljoin(self.mendeley.host, url)
        rsp = super(MendeleySession, self).request(method, full_url, data, headers, **kwargs)

        if rsp.ok:
            return rsp
        else:
            raise MendeleyException(rsp)