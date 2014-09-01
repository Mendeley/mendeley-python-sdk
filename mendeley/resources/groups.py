from mendeley.models.groups import Group, GroupMember

from mendeley.resources.base import ListResource


class Groups(ListResource):
    _url = '/groups'
    _content_type = 'application/vnd.mendeley-group.1+json'
    _obj_type = Group

    def __init__(self, session):
        self.session = session

    def get(self, id):
        url = '/groups/%s' % id
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        return Group(self.session, rsp.json())

    @property
    def _session(self):
        return self.session


class GroupMembers(ListResource):
    _content_type = 'application/vnd.mendeley-membership.1+json'
    _obj_type = GroupMember

    def __init__(self, session, id):
        self.session = session
        self.id = id

    @property
    def _session(self):
        return self.session

    @property
    def _url(self):
        return '/groups/%s/members' % self.id