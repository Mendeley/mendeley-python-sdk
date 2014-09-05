from mendeley.models.profiles import Profile
from mendeley.resources.base import GetByIdResource


class Profiles(GetByIdResource):
    """
    Top-level resource for accessing profiles.
    """
    _url = '/profiles'

    def __init__(self, session):
        self.session = session

    def get(self, id):
        """
        Retrieves a profile by ID.

        :param id: the ID of the profile to get.
        :return: a :class:`Profile <mendeley.models.profiles.Profile>`.
        """
        return super(Profiles, self).get(id)

    @property
    def me(self):
        """
        The :class:`Profile <mendeley.models.profiles.Profile>` of the logged-in user.
        """
        return self.get('me')

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return Profile
