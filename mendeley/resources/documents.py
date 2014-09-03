import json

from mendeley.models.documents import *
from mendeley.resources.base import add_query_params
from mendeley.resources.base_documents import DocumentsBase


class Documents(DocumentsBase):
    _url = '/documents'

    def __init__(self, session, group_id):
        super(Documents, self).__init__(session, group_id)

    def create(self, title, type, **kwargs):
        kwargs['title'] = title
        kwargs['type'] = type
        kwargs['group_id'] = self.group_id

        kwargs = format_args(kwargs)
        content_type = UserDocument.content_type

        rsp = self.session.post(self._url, data=json.dumps(kwargs), headers={
            'Accept': content_type,
            'Content-Type': content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def get(self, id, view=None):
        url = add_query_params('%s/%s' % (self._url, id), {'view': view})
        obj_type = self._view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        return obj_type(self.session, rsp.json())

    def update(self, id, **kwargs):
        url = '%s/%s' % (self._url, id)
        content_type = UserDocument.content_type

        rsp = self.session.patch(url, data=json.dumps(format_args(kwargs)), headers={
            'Accept': content_type,
            'Content-Type': content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def move_to_trash(self, id):
        url = '%s/%s/trash' % (self._url, id)
        self.session.post(url)

    @staticmethod
    def _view_type(view):
        return {
            'all': UserAllDocument,
            'bib': UserBibDocument,
            'client': UserClientDocument,
            'tags': UserTagsDocument,
            'core': UserDocument,
        }.get(view, UserDocument)


def format_args(kwargs):
    if 'authors' in kwargs:
        kwargs['authors'] = [author.json for author in kwargs['authors']]
    if 'editors' in kwargs:
        kwargs['editors'] = [editor.json for editor in kwargs['editors']]
    if 'accessed' in kwargs:
        kwargs['accessed'] = arrow.get(kwargs['accessed']).format('YYYY-MM-DD')

    return kwargs
