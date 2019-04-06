import platform

from future.moves.urllib.parse import urljoin
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session

from mendeley.exception import MendeleyApiException
from mendeley.resources import *
from mendeley.version import __version__


class MendeleySession(OAuth2Session):
    """
    Entry point for accessing Mendeley resources.

    .. attribute:: annotations

        A :class: `Annotations <mendeley.resources.annotations.Annotations>` resource for accessing annotations in the
        logged-in user's library.

    .. attribute:: catalog

       A :class:`Catalog <mendeley.resources.catalog.Catalog>` resource for accessing the Mendeley catalog.

    .. attribute:: documents

       A :class:`Documents <mendeley.resources.documents.Documents>` resource for accessing documents in the logged-in
       user's library.

    .. attribute:: files

       A :class:`Files <mendeley.resources.files.Files>` resource for accessing files in the logged-in user's library.

    .. attribute:: groups

       A :class:`Groups <mendeley.resources.groups.Groups>` resource for accessing groups that the user is a member of.

    .. attribute:: profiles

       A :class:`Profiles <mendeley.resources.profiles.Profiles>` resource for accessing profiles of Mendeley users.

    .. attribute:: trash

       A :class:`Trash <mendeley.resources.trash.Trash>` resource for accessing trashed documents in the logged-in
       user's library.
    """

    def __init__(self, mendeley, token, client=None, refresher=None):
        if client:
            super(MendeleySession, self).__init__(client=client, token=token)
        else:
            super(MendeleySession, self).__init__(client_id=mendeley.client_id, token=token)

        self.host = mendeley.host
        self.refresher = refresher

        self.annotations = Annotations(self)
        self.catalog = Catalog(self)
        self.documents = Documents(self, None)
        self.files = Files(self)
        self.groups = Groups(self)
        self.profiles = Profiles(self)
        self.trash = Trash(self, None)
        self.folders = Folders(self)

    def group_members(self, group_id):
        return GroupMembers(self, group_id)

    def group_documents(self, group_id):
        return Documents(self, group_id)

    def group_trash(self, group_id):
        return Trash(self, group_id)

    def group_folders(self, group_id):
        return Folders(self, group_id)

    def group_files(self, group_id):
        return Files(self, group_id=group_id)

    def document_files(self, document_id):
        return Files(self, document_id=document_id)

    def catalog_files(self, catalog_id):
        return Files(self, catalog_id=catalog_id)

    def folder_documents(self, folder_id, group_id):
        return FolderDocuments(self, folder_id, group_id)

    def request(self, method, url, data=None, headers=None, **kwargs):
        full_url = urljoin(self.host, url)

        if not headers:
            headers = {}

        headers['user-agent'] = self.__user_agent()

        try:
            rsp = self.__do_request(data, full_url, headers, kwargs, method)
        except TokenExpiredError:
            if self.refresher:
                self.refresher.refresh(self)
                rsp = self.__do_request(data, full_url, headers, kwargs, method)
            else:
                raise

        if rsp.ok:
            return rsp
        else:
            raise MendeleyApiException(rsp)

    def __do_request(self, data, full_url, headers, kwargs, method):
        rsp = super(MendeleySession, self).request(method, full_url, data, headers, **kwargs)
        return rsp

    @staticmethod
    def __user_agent():
        return 'mendeley/%s %s/%s %s/%s' % (__version__,
                                            platform.python_implementation(),
                                            platform.python_version(),
                                            platform.system(),
                                            platform.release())
