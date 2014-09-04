from mendeley.models.files import File
from mendeley.resources.base import ListResource


class Files(ListResource):
    _url = '/files'

    def __init__(self, session, catalog_id=None, document_id=None, group_id=None):
        self.session = session
        self.catalog_id = catalog_id
        self.document_id = document_id
        self.group_id = group_id

    def list(self, page_size=None, added_since=None, deleted_since=None):
        return super(Files, self).list(page_size,
                                       added_since=added_since,
                                       deleted_since=deleted_since,
                                       catalog_id=self.catalog_id,
                                       document_id=self.document_id,
                                       group_id=self.group_id)

    def iter(self, page_size=None, added_since=None, deleted_since=None):
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