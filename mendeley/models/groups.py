import arrow

from mendeley.models.common import Photo
from mendeley.models.profiles import LazyProfile
from mendeley.resources.group_members import GroupMembers
from mendeley.response import ResponseObject


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
        return ['id', 'name', 'description', 'disciplines', 'tags', 'webpage', 'link', 'access_level',
                'role']
