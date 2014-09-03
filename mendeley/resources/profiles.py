from mendeley.models.profiles import Profile
from mendeley.resources.base import GetByIdResource


class Profiles(GetByIdResource):
    _url = '/profiles'

    def __init__(self, session):
        self.session = session

    @property
    def me(self):
        return self.get('me')

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return Profile
