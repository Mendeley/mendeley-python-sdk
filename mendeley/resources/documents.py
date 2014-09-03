import json

from mendeley.models.documents import *
from mendeley.resources.base import ListResource, add_query_params


def view_type(view):
    return {
        'all': UserAllDocument,
        'bib': UserBibDocument,
        'client': UserClientDocument,
        'tags': UserTagsDocument,
        'core': UserDocument,
    }.get(view, UserDocument)


class Documents(ListResource):
    _url = '/documents'
    _obj_type = UserDocument

    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        url = add_query_params('%s/%s' % (self._url, id), {'view': view})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        return obj_type(self.session, rsp.json())

    def create(self, title, type, **kwargs):
        kwargs['title'] = title
        kwargs['type'] = type

        if 'authors' in kwargs:
            kwargs['authors'] = [author.json for author in kwargs['authors']]

        if 'editors' in kwargs:
            kwargs['editors'] = [editor.json for editor in kwargs['editors']]

        if 'accessed' in kwargs:
            kwargs['accessed'] = arrow.get(kwargs['accessed']).format('YYYY-MM-DD')

        rsp = self.session.post(self._url, data=json.dumps(kwargs), headers={
            'Accept': self._obj_type.content_type,
            'Content-Type': self._obj_type.content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def delete(self, id):
        url = '%s/%s' % (self._url, id)
        self.session.delete(url)

    @property
    def _session(self):
        return self.session
