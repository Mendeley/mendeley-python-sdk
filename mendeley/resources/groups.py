from mendeley.models import Group


class Groups(object):
    def __init__(self, session):
        self.session = session

    def list(self):
        url = '/groups'
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-group.1+json'})

        return [Group(self.session, g) for g in rsp.json()]
