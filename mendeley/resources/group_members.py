import arrow

from mendeley.resources.profiles import Profile

from mendeley.response import ResponseObject, LazyResponseObject


class GroupMembers(object):
    def __init__(self, session, id):
        self.session = session
        self.id = id

    def list(self):
        url = '/groups/%s/members' % self.id
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-membership.1+json'})

        return [GroupMember(self.session, m) for m in rsp.json()]


class GroupMember(ResponseObject):
    def __init__(self, session, json):
        super(GroupMember, self).__init__(session, json)

        loader = lambda: session.profiles.get(self.id)
        self.__profile = LazyResponseObject(self.id, loader, Profile)

    @property
    def id(self):
        return self.json.get('profile_id')

    @property
    def joined(self):
        if 'joined' in self.json:
            return arrow.get(self.json['joined'])
        else:
            return None

    def __getattr__(self, name):
        if name in dir(self.__profile):
            return getattr(self.__profile, name)
        else:
            return super(GroupMember, self).__getattr__(name)

    @classmethod
    def fields(cls):
        return ['role']