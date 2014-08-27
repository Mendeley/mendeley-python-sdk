import arrow

from mendeley.models import Photo
from mendeley.resources.base import ListResource
from mendeley.resources.group_members import GroupMembers
from mendeley.resources.profiles import LazyProfile
from mendeley.response import ResponseObject


class Groups(ListResource):
    def __init__(self, session):
        super(Groups, self).__init__(session,
                                     '/groups',
                                     'application/vnd.mendeley-group.1+json',
                                     Group)

    def get(self, id):
        url = '/groups/%s' % id
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-group.1+json'})

        return Group(self.session, rsp.json())


class Group(ResponseObject):
    @property
    def created(self):
        if 'created' in self._json:
            return arrow.get(self._json['created'])
        else:
            return None

    @property
    def photo(self):
        if 'photo' in self._json:
            return Photo(self.session, self._json['photo'])
        else:
            return None

    @property
    def owner(self):
        if 'owning_profile_id' in self._json:
            return LazyProfile(self.session, self._json['owning_profile_id'])
        else:
            return None

    @property
    def members(self):
        return GroupMembers(self.session, self.id)

    @classmethod
    def fields(cls):
        return ['id', 'name', 'description', 'disciplines', 'tags', 'webpage', 'created', 'link', 'access_level',
                'role']