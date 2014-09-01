import arrow
from mendeley.models.profiles import LazyProfile

__author__ = 'matt'


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