from mendeley.models.groups import Group, GroupMember

from mendeley.resources.base import ListResource, GetByIdResource


class Groups(GetByIdResource, ListResource):
    _url = '/groups'

    def __init__(self, session):
        self.session = session

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return Group


class GroupMembers(ListResource):
    def __init__(self, session, id):
        self.session = session
        self.id = id

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return GroupMember

    @property
    def _url(self):
        return '/groups/%s/members' % self.id