import platform

from future.moves.urllib.parse import urljoin
from requests_oauthlib import OAuth2Session

from mendeley.exception import MendeleyApiException
from mendeley.resources import Catalog, Documents, GroupMembers, Groups, Profiles
from mendeley.version import __version__


class MendeleySession(OAuth2Session):
    def __init__(self, mendeley, access_token, expires_in=None, refresh_token=None):
        super(MendeleySession, self).__init__(client_id=mendeley.client_id,
                                              token=self.__token_dict(access_token, expires_in, refresh_token))
        self.mendeley = mendeley

        self.catalog = Catalog(self)
        self.documents = Documents(self)
        self.groups = Groups(self)
        self.profiles = Profiles(self)

    def group_members(self, id):
        return GroupMembers(self, id)

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

        if not headers:
            headers = {}

        headers['user-agent'] = self.__user_agent()

        rsp = super(MendeleySession, self).request(method, full_url, data, headers, **kwargs)

        if rsp.ok:
            return rsp
        else:
            raise MendeleyApiException(rsp)

    @staticmethod
    def __user_agent():
        return 'mendeley/%s %s/%s %s/%s' % (__version__,
                                            platform.python_implementation(),
                                            platform.python_version(),
                                            platform.system(),
                                            platform.release())