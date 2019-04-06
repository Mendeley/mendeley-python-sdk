import json
from mendeley.models.folders import Folder

from mendeley.resources.base import ListResource, GetByIdResource
from mendeley.response import LazyResponseObject
from mendeley.resources.base_documents import DocumentsBase
from mendeley.models.documents import *

class Folders(GetByIdResource, ListResource):
    """
    Top-level resource for accessing folders.
    """
    _url = '/folders'

    def __init__(self, session, group_id=None):
        self.session = session
        self.group_id = group_id

    def get(self, id):
        """
        Retrieves a folder by ID.

        :param id: the ID of the folder to get.
        :return: a :class:`Folder <mendeley.models.folders.Folder>`.
        """
        return super(Folders, self).get(id, group_id=self.group_id)

    def list(self, page_size=None):
        """
        Retrieves folders that the logged-in user has, as a paginated collection.

        :param page_size: the number of folders to return on each page.  Defaults to 20.
        :return: a :class:`Page <mendeley.pagination.Page>` of :class:`Folders <mendeley.models.folders.Group>`.
        """
        return super(Folders, self).list(page_size, group_id=self.group_id)

    def iter(self, page_size=None):
        """
        Retrieves folders that the logged-in user is a member of, as an iterator.

        :param page_size: the number of folders to retrieve at a time.  Defaults to 20.
        :return: an iterator of :class:`Folders <mendeley.models.folders.Group>`.
        """
        return super(Folders, self).iter(page_size, group_id=self.group_id)

    def create(self, name, parent_id=None):
        """
        Creates a new folder

        :param name: name of the folder.
        :return: a :class:`Folder <mendeley.models.folders.Folder>`.
        """
        kwargs = {}
        kwargs['name'] = name
        kwargs['parent_id'] = parent_id
        kwargs['group_id'] = self.group_id

        content_type = Folder.content_type

        rsp = self.session.post(self._url, data=json.dumps(kwargs), headers={
            'Accept': content_type,
            'Content-Type': content_type
        })

        return Folder(self.session, rsp.json())

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return Folder

class FolderDocuments(DocumentsBase):
    def __init__(self, session, folder_id, group_id):
        super(FolderDocuments, self).__init__(session, group_id)
        self.folder_id = folder_id

    @staticmethod
    def view_type(view):
        return {
            'all': UserAllDocument,
            'bib': UserBibDocument,
            'client': UserClientDocument,
            'tags': UserTagsDocument,
            'core': UserDocument,
        }.get(view, UserDocument)

    @property
    def _url(self):
        return '/folders/{}/documents'.format(self.folder_id)

    def _obj_type(self, **kwargs):
        class LazyDocument(object):
            content_type = 'application/vnd.mendeley-document.1+json'#Folder.content_type #
            def __call__(self2, session, rsp):
                return LazyResponseObject(session, rsp['id'], super(FolderDocuments,self)._obj_type(**kwargs), lambda: session.group_documents(self.group_id).get(rsp['id'], kwargs['view']))
        return LazyDocument()
        