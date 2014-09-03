from mendeley.models.groups import Group, GroupMember

from mendeley.resources.base import ListResource


class Groups(ListResource):
    _url = '/groups'

    def __init__(self, session):
        self.session = session

    def get(self, id):
        url = '/groups/%s' % id
        rsp = self.session.get(url, headers={'Accept': Group.content_type})

        return Group(self.session, rsp.json())

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