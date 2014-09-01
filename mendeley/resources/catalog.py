from mendeley.exception import MendeleyException
from mendeley.models.catalog import *
from mendeley.resources.base import add_query_params, ListResource


def view_type(view):
    return {
        'bib': CatalogBibDocument,
        'client': CatalogClientDocument,
        'stats': CatalogStatsDocument,
        'all': CatalogAllDocument,
        'core': CatalogDocument
    }.get(view, CatalogDocument)


class Catalog(object):
    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        url = add_query_params('/catalog/%s' % id, {'view': view})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        return obj_type(self.session, rsp.json())

    def by_identifier(self, arxiv=None, doi=None, isbn=None, issn=None, pmid=None, scopus=None, filehash=None,
                      view=None):
        url = add_query_params('/catalog', {'arxiv': arxiv, 'doi': doi, 'isbn': isbn, 'issn': issn, 'pmid': pmid,
                                            'scopus': scopus, 'filehash': filehash, 'view': view})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        if len(rsp.json()) == 0:
            raise MendeleyException('Catalog document not found')

        return obj_type(self.session, rsp.json()[0])

    def lookup(self, arxiv=None, doi=None, pmid=None, filehash=None, title=None, authors=None, year=None, source=None,
               view=None):
        url = add_query_params('/metadata', {'arxiv': arxiv, 'doi': doi, 'pmid': pmid, 'filehash': filehash,
                                             'title': title, 'authors': authors, 'year': year, 'source': source})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        return LookupResponse(self.session, rsp.json(), view, obj_type)

    def search(self, query, view=None):
        return CatalogSearch(self.session, query=query, view=view)

    def advanced_search(self, title=None, author=None, source=None, abstract=None, min_year=None, max_year=None,
                        open_access=None, view=None):
        return CatalogSearch(self.session, title=title, author=author, source=source, abstract=abstract,
                             min_year=min_year, max_year=max_year, open_access=open_access, view=view)


class CatalogSearch(ListResource):
    def __init__(self, session, **kwargs):
        self.session = session
        self.params = kwargs

    @property
    def _obj_type(self):
        return view_type(self.params.get('view'))

    @property
    def _url(self):
        return add_query_params('/search/catalog', self.params)

    @property
    def _session(self):
        return self.session