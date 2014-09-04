import json
from mimetypes import guess_type
from os.path import basename

import arrow

from mendeley.models.base_documents import BaseDocument, BaseBibView, BaseClientView
from mendeley.models.files import File
from mendeley.models.groups import LazyGroup
from mendeley.models.profiles import LazyProfile


class UserBaseDocument(BaseDocument):
    @property
    def created(self):
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def last_modified(self):
        if 'last_modified' in self.json:
            return arrow.get(self.json['last_modified'])
        elif 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def profile(self):
        if 'profile_id' in self.json:
            return LazyProfile(self.session, self.json['profile_id'])
        else:
            return None

    @property
    def group(self):
        if 'group_id' in self.json:
            return LazyGroup(self.session, self.json['group_id'])
        else:
            return None

    @property
    def files(self):
        return self.session.document_files(document_id=self.id)


class UserBibView(BaseBibView):
    @property
    def accessed(self):
        if 'accessed' in self.json:
            return arrow.get(self.json['accessed'])
        else:
            return None


class UserClientView(BaseClientView):
    @classmethod
    def fields(cls):
        return super(UserClientView, cls).fields() + ['read', 'starred', 'authored', 'confirmed', 'hidden']


class UserTagsView(object):
    @classmethod
    def fields(cls):
        return ['tags']


class UserDocument(UserBaseDocument):
    def update(self, **kwargs):
        rsp = self.session.patch('/documents/%s' % self.id, data=json.dumps(format_args(kwargs)), headers={
            'Accept': self.content_type,
            'Content-Type': self.content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def delete(self):
        self.session.delete('/documents/%s' % self.id)

    def move_to_trash(self):
        self.session.post('/documents/%s/trash' % self.id)
        return self._trashed_type()(self.session, self.json)

    def attach_file(self, path):
        filename = basename(path)
        headers = {
            'content-disposition': 'attachment; filename=%s' % filename,
            'content-type': guess_type(filename),
            'link': '<%s/documents/%s>; rel="document"' % (self.session.host, self.id),
            'accept': File.content_type
        }

        with open(path) as f:
            rsp = self.session.post('/files', data=f, headers=headers)

        return File(self.session, rsp.json())

    @classmethod
    def _trashed_type(cls):
        return TrashDocument


class UserBibDocument(UserDocument, UserBibView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserBibView.fields()

    @classmethod
    def _trashed_type(cls):
        return TrashBibDocument


class UserClientDocument(UserDocument, UserClientView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserClientView.fields()

    @classmethod
    def _trashed_type(cls):
        return TrashClientDocument


class UserTagsDocument(UserDocument, UserTagsView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserTagsView.fields()

    @classmethod
    def _trashed_type(cls):
        return TrashTagsDocument


class UserAllDocument(UserDocument, UserBibView, UserClientView, UserTagsView):
    @classmethod
    def fields(cls):
        return UserDocument.fields() + UserBibView.fields() + UserClientView.fields() + UserTagsView.fields()

    @classmethod
    def _trashed_type(cls):
        return TrashAllDocument


class TrashDocument(UserBaseDocument):
    def delete(self):
        url = '/trash/%s' % self.id
        self.session.delete(url)

    def restore(self):
        self.session.post('/trash/%s/restore' % self.id)
        return self._restored_type()(self.session, self.json)

    @classmethod
    def _restored_type(cls):
        return UserDocument


class TrashAllDocument(TrashDocument, UserBibView, UserClientView, UserTagsView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserBibView.fields() + UserClientView.fields() + UserTagsView.fields()

    @classmethod
    def _restored_type(cls):
        return UserAllDocument


class TrashTagsDocument(TrashDocument, UserTagsView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserTagsView.fields()

    @classmethod
    def _restored_type(cls):
        return UserTagsDocument


class TrashClientDocument(TrashDocument, UserClientView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserClientView.fields()

    @classmethod
    def _restored_type(cls):
        return UserClientDocument


class TrashBibDocument(TrashDocument, UserBibView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserBibView.fields()

    @classmethod
    def _restored_type(cls):
        return UserBibDocument


def format_args(kwargs):
    if 'authors' in kwargs:
        kwargs['authors'] = [author.json for author in kwargs['authors']]
    if 'editors' in kwargs:
        kwargs['editors'] = [editor.json for editor in kwargs['editors']]
    if 'accessed' in kwargs:
        kwargs['accessed'] = arrow.get(kwargs['accessed']).format('YYYY-MM-DD')

    return kwargs