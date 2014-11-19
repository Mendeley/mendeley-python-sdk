from mendeley.exception import MendeleyException
from mendeley.models.catalog import *
from mendeley.resources.base import add_query_params, ListResource, GetByIdResource


class Catalog(GetByIdResource):
    """
    Top-level resource for accessing catalog documents.
    """
    _url = '/catalog'

    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        """
        Retrieves a catalog document by ID.

        :param id: the ID of the document to get.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>`.
        """
        return super(Catalog, self).get(id, view=view)

    def by_identifier(self, arxiv=None, doi=None, isbn=None, issn=None, pmid=None, scopus=None, filehash=None,
                      view=None):
        """
        Retrieves a catalog document by an external identifier.  Only one identifier may be specified.

        :param arxiv: ArXiV ID.
        :param doi: DOI.
        :param isbn: ISBN.
        :param issn: ISSN.
        :param pmid: PubMed ID.
        :param scopus: Scopus ID (EID).
        :param filehash: SHA-1 filehash.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>`.
        """
        url = add_query_params('/catalog', {'arxiv': arxiv, 'doi': doi, 'isbn': isbn, 'issn': issn, 'pmid': pmid,
                                            'scopus': scopus, 'filehash': filehash, 'view': view})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        if len(rsp.json()) == 0:
            raise MendeleyException('Catalog document not found')

        return obj_type(self.session, rsp.json()[0])

    def lookup(self, arxiv=None, doi=None, pmid=None, filehash=None, title=None, authors=None, year=None, source=None,
               view=None):
        """
        Finds the closest matching catalog document to a supplied set of metadata.

        :param arxiv: ArXiV ID.
        :param doi: DOI.
        :param pmid: PubMed ID.
        :param filehash: SHA-1 filehash.
        :param title: Title.
        :param authors: Authors.
        :param year: Year.
        :param source: Source.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>`.
        """
        url = add_query_params('/metadata', {'arxiv': arxiv, 'doi': doi, 'pmid': pmid, 'filehash': filehash,
                                             'title': title, 'authors': authors, 'year': year, 'source': source})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        return LookupResponse(self.session, rsp.json(), view, obj_type)

    def search(self, query, view=None):
        """
        Searches the catalog for documents.

        :param query: the search query to execute.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`CatalogSearch <mendeley.models.catalog.CatalogSearch>` resource, from which results can be
                 retrieved.
        """
        return CatalogSearch(self.session, query=query, view=view)

    def advanced_search(self, title=None, author=None, source=None, abstract=None, min_year=None, max_year=None,
                        open_access=None, view=None):
        """
        Executes an advanced catalog search, where individual fields can be searched on.

        :param title: Title.
        :param author: Author.
        :param source: Source.
        :param abstract: Abstract.
        :param min_year: Minimum year for documents to return.
        :param max_year: Maximum year for documents to return.
        :param open_access: If 'true', only returns open access documents.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`CatalogSearch <mendeley.models.catalog.CatalogSearch>` resource, from which results can be
                 retrieved.
        """
        return CatalogSearch(self.session, title=title, author=author, source=source, abstract=abstract,
                             min_year=min_year, max_year=max_year, open_access=open_access, view=view)

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return view_type(kwargs.get('view'))


class CatalogSearch(ListResource):
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
        return super(CatalogSearch, self).list(page_size)

    def iter(self, page_size=None):
        """
        Retrieves search results, as an iterator.

        :param page_size: the number of search results to retrieve at a time.  Defaults to 20.
        :return: an iterator of :class:`CatalogDocuments <mendeley.models.catalog.CatalogDocument>`.
        """
        return super(CatalogSearch, self).iter(page_size)

    def _obj_type(self, **kwargs):
        return view_type(self.params['view'])

    @property
    def _url(self):
        return add_query_params('/search/catalog', self.params)

    @property
    def _session(self):
        return self.session


def view_type(view):
    return {
        'bib': CatalogBibDocument,
        'client': CatalogClientDocument,
        'stats': CatalogStatsDocument,
        'all': CatalogAllDocument,
        'core': CatalogDocument
    }.get(view, CatalogDocument)