import arrow

from mendeley.resources.base import ListResource

from mendeley.resources.profiles import LazyProfile


class GroupMembers(ListResource):
    def __init__(self, session, id):
        super(GroupMembers, self).__init__(session,
                                           '/groups/%s/members' % id,
                                           'application/vnd.mendeley-membership.1+json',
                                           GroupMember)


class GroupMember(LazyProfile):
    def __init__(self, session, member_json):
        super(GroupMember, self).__init__(session, member_json.get('profile_id'))

        self.member_json = member_json

    @property
    def joined(self):
        if 'joined' in self.member_json:
            return arrow.get(self.member_json['joined'])
        else:
            return None

    @property
    def role(self):
        return self.member_json.get('role')