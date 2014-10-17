import json
from mimetypes import guess_type
from os.path import basename

import arrow

from mendeley.models.base_documents import BaseDocument, BaseBibView, BaseClientView
from mendeley.models.files import File


class UserBaseDocument(BaseDocument):
    @property
    def created(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def last_modified(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'last_modified' in self.json:
            return arrow.get(self.json['last_modified'])
        elif 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def profile(self):
        """
        a :class:`Profile <mendeley.models.profiles.Profile>`.
        """
        if 'profile_id' in self.json:
            return self.session.profiles.get_lazy(self.json['profile_id'])
        else:
            return None

    @property
    def group(self):
        """
        a :class:`Group <mendeley.models.groups.Group>`.
        """
        if 'group_id' in self.json:
            return self.session.groups.get_lazy(self.json['group_id'])
        else:
            return None

    @property
    def files(self):
        """
        a :class:`Files <mendeley.resources.files.Files>` resource, from which
        :class:`Files <mendeley.models.files.File>` can be retrieved.
        """
        return self.session.document_files(document_id=self.id)


class UserBibView(BaseBibView):
    """
    Additional fields returned when getting a :class:`UserDocument <mendeley.models.documents.UserDocument>` or
    :class:`TrashDocument <mendeley.models.documents.TrashDocument>` with view='bib' or 'all'.

    .. attribute:: pages
    .. attribute:: volume
    .. attribute:: issue
    .. attribute:: websites
    .. attribute:: month
    .. attribute:: publisher
    .. attribute:: day
    .. attribute:: city
    .. attribute:: edition
    .. attribute:: institution
    .. attribute:: series
    .. attribute:: chapter
    .. attribute:: revision
    """
    @property
    def accessed(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'accessed' in self.json:
            return arrow.get(self.json['accessed'])
        else:
            return None


class UserClientView(BaseClientView):
    """
    Additional fields returned when getting a :class:`UserDocument <mendeley.models.documents.UserDocument>` or
    :class:`TrashDocument <mendeley.models.documents.TrashDocument>` with view='client' or 'all'.

    .. attribute:: file_attached
    .. attribute:: read
    .. attribute:: starred
    .. attribute:: authored
    .. attribute:: confirmed
    .. attribute:: hidden
    """
    @classmethod
    def fields(cls):
        return super(UserClientView, cls).fields() + ['read', 'starred', 'authored', 'confirmed', 'hidden']


class UserTagsView(object):
    """
    Additional fields returned when getting a :class:`UserDocument <mendeley.models.documents.UserDocument>` or
    :class:`TrashDocument <mendeley.models.documents.TrashDocument>` with view='tags' or 'all'.

    .. attribute:: tags
    """
    @classmethod
    def fields(cls):
        return ['tags']


class UserDocument(UserBaseDocument):
    """
    Base class for user documents.

    .. attribute:: id
    .. attribute:: title
    .. attribute:: type
    .. attribute:: source
    .. attribute:: year
    .. attribute:: identifiers
    .. attribute:: keywords
    .. attribute:: abstract
    """
    def update(self, **kwargs):
        """
        Updates this document.

        :param kwargs: updated field values.  Only the values supplied will be modified.
        :return: the updated document.
        """
        rsp = self.session.patch('/documents/%s' % self.id, data=json.dumps(format_args(kwargs)), headers={
            'Accept': self.content_type,
            'Content-Type': self.content_type
        })

        return UserAllDocument(self.session, rsp.json())

    def delete(self):
        """
        Permanently deletes this document.
        """
        self.session.delete('/documents/%s' % self.id)

    def move_to_trash(self):
        """
        Moves this document to the trash.

        :return: a :class:`TrashDocument <mendeley.models.documents.TrashDocument>`.
        """
        self.session.post('/documents/%s/trash' % self.id)
        return self._trashed_type()(self.session, self.json)

    def attach_file(self, path):
        """
        Attaches a file to this document.

        :param path: the path of the file to attach.
        :return: a :class:`File <mendeley.models.files.File>`.
        """
        filename = basename(path)
        headers = {
            'content-disposition': 'attachment; filename=%s' % filename,
            'content-type': guess_type(filename)[0],
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
    """
    Base class for trashed documents.

    .. attribute:: id
    .. attribute:: title
    .. attribute:: type
    .. attribute:: source
    .. attribute:: year
    .. attribute:: identifiers
    .. attribute:: keywords
    .. attribute:: abstract
    """

    def delete(self):
        """
        Permanently deletes this document.
        """
        url = '/trash/%s' % self.id
        self.session.delete(url)

    def restore(self):
        """
        Restores this document from the trash.

        :return: a :class:`UserDocument <mendeley.models.documents.UserDocument>`.
        """
        self.session.post('/trash/%s/restore' % self.id)
        return self._restored_type()(self.session, self.json)

    @classmethod
    def _restored_type(cls):
        return UserDocument


class TrashBibDocument(TrashDocument, UserBibView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserBibView.fields()

    @classmethod
    def _restored_type(cls):
        return UserBibDocument


class TrashClientDocument(TrashDocument, UserClientView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserClientView.fields()

    @classmethod
    def _restored_type(cls):
        return UserClientDocument


class TrashTagsDocument(TrashDocument, UserTagsView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserTagsView.fields()

    @classmethod
    def _restored_type(cls):
        return UserTagsDocument


class TrashAllDocument(TrashDocument, UserBibView, UserClientView, UserTagsView):
    @classmethod
    def fields(cls):
        return TrashDocument.fields() + UserBibView.fields() + UserClientView.fields() + UserTagsView.fields()

    @classmethod
    def _restored_type(cls):
        return UserAllDocument


def format_args(kwargs):
    if 'authors' in kwargs:
        kwargs['authors'] = [author.json for author in kwargs['authors']]
    if 'editors' in kwargs:
        kwargs['editors'] = [editor.json for editor in kwargs['editors']]
    if 'accessed' in kwargs:
        kwargs['accessed'] = arrow.get(kwargs['accessed']).format('YYYY-MM-DD')

    return kwargs