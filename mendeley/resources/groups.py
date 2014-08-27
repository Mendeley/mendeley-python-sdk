import arrow
from mendeley.models import Photo
from mendeley.resources.group_members import GroupMembers
from mendeley.resources.profiles import Profile
from mendeley.response import ResponseObject, LazyResponseObject


class Groups(object):
    def __init__(self, session):
        self.session = session

    def list(self):
        url = '/groups'
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-group.1+json'})

        return [Group(self.session, g) for g in rsp.json()]

    def get(self, id):
        url = '/groups/%s' % id
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-group.1+json'})

        return Group(self.session, rsp.json())


class Group(ResponseObject):
    @property
    def created(self):
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def photo(self):
        if 'photo' in self.json:
            return Photo(self.session, self.json['photo'])
        else:
            return None

    @property
    def owner(self):
        if 'owning_profile_id' in self.json:
            profile_id = self.json['owning_profile_id']
            loader = lambda: self.session.profiles.get(profile_id)
            return LazyResponseObject(profile_id, loader, Profile)
        else:
            return None

    @property
    def members(self):
        return GroupMembers(self.session, self.id)

    @classmethod
    def fields(cls):
        return ['id', 'name', 'description', 'disciplines', 'tags', 'webpage', 'created', 'link', 'access_level',
                'role']