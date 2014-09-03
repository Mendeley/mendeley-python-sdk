import json

from mendeley.models.documents import *
from mendeley.resources.base import ListResource, add_query_params


class Documents(ListResource):
    _url = '/documents'

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

        kwargs = format_args(kwargs)
        content_type = UserDocument.content_type

        rsp = self.session.post(self._url, data=json.dumps(kwargs), headers={
            'Accept': content_type,
            'Content-Type': content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def update(self, id, **kwargs):
        url = '%s/%s' % (self._url, id)
        content_type = UserDocument.content_type

        rsp = self.session.patch(url, data=json.dumps(kwargs), headers={
            'Accept': content_type,
            'Content-Type': content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def delete(self, id):
        url = '%s/%s' % (self._url, id)
        self.session.delete(url)

    def list(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None):
        return super(Documents, self).list(page_size,
                                           view=view,
                                           sort=sort,
                                           order=order,
                                           modified_since=modified_since,
                                           deleted_since=deleted_since)

    def iter(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None):
        return super(Documents, self).iter(page_size,
                                           view=view,
                                           sort=sort,
                                           order=order,
                                           modified_since=modified_since,
                                           deleted_since=deleted_since)

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return view_type(kwargs.get('view'))


def view_type(view):
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
