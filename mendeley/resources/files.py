from mendeley.models.files import File
from mendeley.resources.base import ListResource


class Files(ListResource):
    """
    Top-level resource for accessing files.  These can be:

    - files for the logged-in user, if retrieved from a
      :func:`MendeleySession <mendeley.session.MendeleySession.files>`.
    - files attached to a :func:`CatalogDocument <mendeley.models.catalog.CatalogDocument.files>`.
    - files attached to a :func:`UserDocument <mendeley.models.documents.UserDocument.files>`.
    - files in a :func:`Group <mendeley.models.groups.Group.files>`.
    """
    _url = '/files'

    def __init__(self, session, catalog_id=None, document_id=None, group_id=None):
        self.session = session
        self.catalog_id = catalog_id
        self.document_id = document_id
        self.group_id = group_id

    def get(self, id):
        """
        Retrieves a file by ID.

        :param id: the ID of the file to get.
        :return: a :class:`File <mendeley.models.files.File>`.
        """
        return super(Files, self).get(id)

    def list(self, page_size=None, added_since=None, deleted_since=None):
        """
        Retrieves files, as a paginated collection.

        :param page_size: the number of files to return on each page.  Defaults to 20.
        :param added_since: if specified, only returns files added after this timestamp.
        :param deleted_since: if specified, only returns the IDs of files deleted after this timestamp.
        :return: a :class:`Page <mendeley.pagination.Page>` of :class:`Files <mendeley.models.files.File>`.
        """
        return super(Files, self).list(page_size,
                                       added_since=added_since,
                                       deleted_since=deleted_since,
                                       catalog_id=self.catalog_id,
                                       document_id=self.document_id,
                                       group_id=self.group_id)

    def iter(self, page_size=None, added_since=None, deleted_since=None):
        """
        Retrieves files, as an iterator.

        :param page_size: the number of files to retrieve at a time.  Defaults to 20.
        :param added_since: if specified, only returns files added after this timestamp.
        :param deleted_since: if specified, only returns the IDs of files deleted after this timestamp.
        :return: an iterator of :class:`Files <mendeley.models.files.File>`.
        """
        return super(Files, self).iter(page_size,
                                       added_since=added_since,
                                       deleted_since=deleted_since,
                                       catalog_id=self.catalog_id,
                                       document_id=self.document_id,
                                       group_id=self.group_id)

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return File