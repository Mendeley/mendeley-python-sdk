from mendeley.models.documents import TrashAllDocument, TrashBibDocument, TrashClientDocument, TrashTagsDocument, \
    TrashDocument
from mendeley.resources.base_documents import DocumentsBase


class Trash(DocumentsBase):
    """
    Top-level resource for accessing trashed documents.  These can be:

    - trashed documents for the logged-in user, if retrieved from a
      :func:`MendeleySession <mendeley.session.MendeleySession.trash>`.
    - trashed documents in a :func:`Group <mendeley.models.groups.Group.trash>`.
    """
    _url = '/trash'

    def __init__(self, session, group_id):
        super(Trash, self).__init__(session, group_id)

    def get(self, id, view=None):
        """
        Retrieves a trashed document by ID.

        :param id: the ID of the document to get.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :return: a :class:`TrashDocument <mendeley.models.documents.TrashDocument>`.
        """
        return super(Trash, self).get(id, view)

    def list(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None):
        """
        Retrieves trashed documents, as a paginated collection.

        :param page_size: the number of documents to return on each page.  Defaults to 20.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :param sort: if specified, sorts documents by the specified field.  One of 'created', 'last_modified', 'title'.
        :param order: if specified in conjunction with 'sort', specifies the sort order.  One of 'asc', 'desc'.
        :param modified_since: if specified, only returns files modified after this timestamp.
        :param deleted_since: if specified, only returns the IDs of documents deleted after this timestamp.
        :return: a :class:`Page <mendeley.pagination.Page>` of
                 :class:`TrashDocuments <mendeley.models.documents.TrashDocument>`.
        """
        return super(Trash, self).list(page_size, view, sort, order, modified_since, deleted_since)

    def iter(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None):
        """
        Retrieves trashed documents, as an iterator.

        :param page_size: the number of documents to retrieve at a time.  Defaults to 20.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :param sort: if specified, sorts documents by the specified field.  One of 'created', 'last_modified', 'title'.
        :param order: if specified in conjunction with 'sort', specifies the sort order.  One of 'asc', 'desc'.
        :param modified_since: if specified, only returns files modified after this timestamp.
        :param deleted_since: if specified, only returns the IDs of documents deleted after this timestamp.
        :return: an iterator of :class:`TrashDocuments <mendeley.models.documents.TrashDocument>`.
        """
        return super(Trash, self).iter(page_size, view, sort, order, modified_since, deleted_since)

    @staticmethod
    def _view_type(view):
        return {
            'all': TrashAllDocument,
            'bib': TrashBibDocument,
            'client': TrashClientDocument,
            'tags': TrashTagsDocument,
            'core': TrashDocument,
        }.get(view, TrashDocument)
