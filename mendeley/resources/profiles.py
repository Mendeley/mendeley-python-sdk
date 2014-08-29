import arrow
from mendeley.models import Discipline, Photo, Location, Education, Employment
from mendeley.response import ResponseObject, LazyResponseObject


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


class Profile(ResponseObject):
    @property
    def created(self):
        if 'created' in self._json:
            return arrow.get(self._json['created'])
        else:
            return None

    @property
    def discipline(self):
        if 'discipline' in self._json:
            return Discipline(self.session, self._json['discipline'])
        else:
            return None

    @property
    def photo(self):
        if 'photo' in self._json:
            return Photo(self.session, self._json['photo'])
        else:
            return None

    @property
    def location(self):
        if 'location' in self._json:
            return Location(self.session, self._json['location'])
        else:
            return None

    @property
    def education(self):
        if 'education' in self._json:
            return [Education(self.session, e) for e in self._json['education']]
        else:
            return None

    @property
    def employment(self):
        if 'employment' in self._json:
            return [Employment(self.session, e) for e in self._json['employment']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'first_name', 'last_name', 'display_name', 'email', 'link', 'research_interests',
                'academic_status', 'verified', 'user_type']


class LazyProfile(LazyResponseObject):
    def __init__(self, session, id):
        super(LazyProfile, self).__init__(session, id, Profile)

    def _load(self):
        url = '/profiles/%s' % self.id
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-profiles.1+json'})

        return rsp.json()
