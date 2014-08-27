import arrow
from mendeley.models import Discipline, Photo, Location, Education, Employment
from mendeley.response import ResponseObject


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
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def discipline(self):
        if 'discipline' in self.json:
            return Discipline(self.session, self.json['discipline'])
        else:
            return None

    @property
    def photo(self):
        if 'photo' in self.json:
            return Photo(self.session, self.json['photo'])
        else:
            return None

    @property
    def location(self):
        if 'location' in self.json:
            return Location(self.session, self.json['location'])
        else:
            return None

    @property
    def education(self):
        if 'education' in self.json:
            return [Education(self.session, e) for e in self.json['education']]
        else:
            return None

    @property
    def employment(self):
        if 'employment' in self.json:
            return [Employment(self.session, e) for e in self.json['employment']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'first_name', 'last_name', 'display_name', 'email', 'link', 'research_interests',
                'academic_status', 'verified', 'user_type']