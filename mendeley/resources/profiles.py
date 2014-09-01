from mendeley.models.profiles import Profile


class Profiles(object):
    def __init__(self, session):
        self.session = session

    @property
    def me(self):
        return self.get('me')

    def get(self, profile_id):
        url = '/profiles/%s' % profile_id
        rsp = self.session.get(url, headers={'Accept': Profile.content_type})

        return Profile(self.session, rsp.json())
