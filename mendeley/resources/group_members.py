from mendeley.models.group_members import GroupMember
from mendeley.resources.base import ListResource


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
