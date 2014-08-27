from mendeley.models import Profile


class Profiles(object):
    def __init__(self, session):
        self.session = session

    @property
    def me(self):
        return self.get('me')

    def get(self, profile_id):
        url = '/profiles/%s' % profile_id
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-profiles.1+json'})

        return Profile(self.session, rsp.json())
