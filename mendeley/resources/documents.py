from mendeley.exception import MendeleyException
from mendeley.models.documents import *
from mendeley.resources.base import add_query_params, ListResource
from mendeley.resources.base_documents import DocumentsBase


class Documents(DocumentsBase):
    """
    Top-level resource for accessing documents.  These can be:

    - documents for the logged-in user, if retrieved from a
      :func:`MendeleySession <mendeley.session.MendeleySession.documents>`.
    - documents in a :func:`Group <mendeley.models.groups.Group.documents>`.
    """
    _url = '/documents'

    def __init__(self, session, group_id):
        super(Documents, self).__init__(session, group_id)

    def get(self, id, view=None):
        """
        Retrieves a document by ID.

        :param id: the ID of the document to get.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :return: a :class:`UserDocument <mendeley.models.documents.UserDocument>`.
        """
        return super(Documents, self).get(id, view)

    def list(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None):
        """
        Retrieves documents, as a paginated collection.

        :param page_size: the number of documents to return on each page.  Defaults to 20.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :param sort: if specified, sorts documents by the specified field.  One of 'created', 'last_modified', 'title'.
        :param order: if specified in conjunction with 'sort', specifies the sort order.  One of 'asc', 'desc'.
        :param modified_since: if specified, only returns files modified after this timestamp.
        :param deleted_since: if specified, only returns the IDs of documents deleted after this timestamp.
        :return: a :class:`Page <mendeley.pagination.Page>` of
                 :class:`UserDocuments <mendeley.models.documents.UserDocument>`.
        """
        return super(Documents, self).list(page_size, view, sort, order, modified_since, deleted_since)

    def iter(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None):
        """
        Retrieves documents, as an iterator.

        :param page_size: the number of documents to retrieve at a time.  Defaults to 20.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :param sort: if specified, sorts documents by the specified field.  One of 'created', 'last_modified', 'title'.
        :param order: if specified in conjunction with 'sort', specifies the sort order.  One of 'asc', 'desc'.
        :param modified_since: if specified, only returns files modified after this timestamp.
        :param deleted_since: if specified, only returns the IDs of documents deleted after this timestamp.
        :return: an iterator of :class:`UserDocuments <mendeley.models.documents.UserDocument>`.
        """
        return super(Documents, self).iter(page_size, view, sort, order, modified_since, deleted_since)

    def create(self, title, type, **kwargs):
        """
        Creates a new document from metadata.

        :param title: title of the document.
        :param type: type of the document.
        :param kwargs: other properties of the document.  These can be any of the attributes on
               :class:`UserDocument <mendeley.models.documents.UserDocument>` or any of its views.
        :return: a :class:`UserDocument <mendeley.models.documents.UserDocument>`.
        """
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

    def create_from_file(self, path):
        """
        Creates a new document from a file.

        :param path: path to the file.
        :return: a :class:`UserDocument <mendeley.models.documents.UserDocument>`.
        """
        filename = basename(path)
        headers = {
            'content-disposition': 'attachment; filename=%s' % filename,
            'content-type': guess_type(filename)[0],
            'accept': UserDocument.content_type
        }

        with open(path, 'rb') as f:
            rsp = self.session.post('/documents', data=f, headers=headers)

        return UserAllDocument(self.session, rsp.json())

    def search(self, query, view=None):
        """
        Searches the logged-in user's library for documents.

        :param query: the search query to execute.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :return: a :class:`DocumentsSearch <mendeley.models.documents.DocumentsSearch>` resource, from which results can
                 be retrieved.
        """
        if self.group_id:
            raise MendeleyException('Search is not available for group documents')

        return DocumentsSearch(self.session, query=query, view=view)

    def advanced_search(self, title=None, author=None, source=None, abstract=None, min_year=None, max_year=None,
                        view=None):
        """
        Executes an advanced search in the logged-in user's library, where individual fields can be searched on.

        :param title: Title.
        :param author: Author.
        :param source: Source.
        :param abstract: Abstract.
        :param min_year: Minimum year for documents to return.
        :param max_year: Maximum year for documents to return.
        :param view: the view to get.  One of 'bib', 'client', 'tags', 'all'.
        :return: a :class:`DocumentsSearch <mendeley.models.documents.DocumentsSearch>` resource, from which results can
                 be retrieved.
        """
        if self.group_id:
            raise MendeleyException('Search is not available for group documents')

        return DocumentsSearch(self.session, title=title, author=author, source=source, abstract=abstract,
                               min_year=min_year, max_year=max_year, view=view)

    @staticmethod
    def view_type(view):
        return {
            'all': UserAllDocument,
            'bib': UserBibDocument,
            'client': UserClientDocument,
            'tags': UserTagsDocument,
            'core': UserDocument,
        }.get(view, UserDocument)


class DocumentsSearch(ListResource):
    """
    Resource for accessing the results of a catalog search.
    """

    def __init__(self, session, **kwargs):
        self.session = session
        self.params = kwargs

    def list(self, page_size=None):
        """
        Retrieves search results, as a paginated collection.

        :param page_size: the number of search results to return on each page.  Defaults to 20.
        :return: a :class:`Page <mendeley.pagination.Page>` of
                 :class:`CatalogDocuments <mendeley.models.catalog.CatalogDocument>`.
        """
        return super(DocumentsSearch, self).list(page_size)

    def iter(self, page_size=None):
        """
        Retrieves search results, as an iterator.

        :param page_size: the number of search results to retrieve at a time.  Defaults to 20.
        :return: an iterator of :class:`CatalogDocuments <mendeley.models.catalog.CatalogDocument>`.
        """
        return super(DocumentsSearch, self).iter(page_size)

    def _obj_type(self, **kwargs):
        return Documents.view_type(self.params['view'])

    @property
    def _url(self):
        return add_query_params('/search/documents', self.params)

    @property
    def _session(self):
        return self.session
