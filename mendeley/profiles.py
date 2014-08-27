import arrow

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

        if rsp.ok:
            return Profile(self.session, rsp.json())
        else:
            return None


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


class Discipline(ResponseObject):
    @classmethod
    def fields(cls):
        return ['name', 'subdisciplines']


class Photo(ResponseObject):
    @classmethod
    def fields(cls):
        return ['original', 'standard', 'square']


class Location(ResponseObject):
    @classmethod
    def fields(cls):
        return ['latitude', 'longitude', 'name']


class Education(ResponseObject):
    @property
    def start_date(self):
        if 'start_date' in self.json:
            return arrow.get(self.json['start_date'])
        else:
            return

    @property
    def end_date(self):
        if 'end_date' in self.json:
            return arrow.get(self.json['end_date'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['institution', 'degree', 'website']


class Employment(ResponseObject):
    @property
    def start_date(self):
        if 'start_date' in self.json:
            return arrow.get(self.json['start_date'])
        else:
            return

    @property
    def end_date(self):
        if 'end_date' in self.json:
            return arrow.get(self.json['end_date'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['institution', 'position', 'website', 'classes']