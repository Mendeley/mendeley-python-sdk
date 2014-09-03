import json

from mendeley.models.documents import UserDocument
from mendeley.resources.base import ListResource


class Documents(ListResource):
    _url = '/documents'
    _obj_type = UserDocument

    def __init__(self, session):
        self.session = session

    def create(self, title, type):
        doc = {'title': title, 'type': type}
        rsp = self.session.post(self._url, data=json.dumps(doc), headers={
            'Accept': self._obj_type.content_type,
            'Content-Type': self._obj_type.content_type
        })

        return UserDocument(self.session, rsp.json())

    def delete(self, id):
        url = '%s/%s' % (self._url, id)
        self.session.delete(url)

    @property
    def _session(self):
        return self.session
