import arrow

from mendeley.models.common import Discipline, Photo, Location, Education, Employment
from mendeley.response import ResponseObject, LazyResponseObject, SessionResponseObject


class Profile(SessionResponseObject):
    content_type = 'application/vnd.mendeley-profiles.1+json'

    @property
    def created(self):
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def discipline(self):
        if 'discipline' in self.json:
            return Discipline(self.json['discipline'])
        else:
            return None

    @property
    def photo(self):
        if 'photo' in self.json:
            return Photo(self.json['photo'])
        else:
            return None

    @property
    def location(self):
        if 'location' in self.json:
            return Location(self.json['location'])
        else:
            return None

    @property
    def education(self):
        if 'education' in self.json:
            return [Education(e) for e in self.json['education']]
        else:
            return None

    @property
    def employment(self):
        if 'employment' in self.json:
            return [Employment(e) for e in self.json['employment']]
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
