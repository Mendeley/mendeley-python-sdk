from future.utils import iteritems

from mendeley.exception import MendeleyException
from mendeley.models.catalog import *
from mendeley.resources.base import add_query_params, ListResource


def view_type(view):
    return {
        'bib': CatalogBibDocument,
        'client': CatalogClientDocument,
        'stats': CatalogStatsDocument,
        'all': CatalogAllDocument,
        'core': CatalogCoreDocument
    }.get(view, CatalogCoreDocument)


class Catalog(object):
    _content_type = 'application/vnd.mendeley-document.1+json'

    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        url = add_query_params('/catalog/%s' % id, {'view': view})
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        return view_type(view)(self.session, rsp.json())

    def by_identifier(self, arxiv=None, doi=None, isbn=None, issn=None, pmid=None, scopus=None, filehash=None,
                      view=None):
        (name, value) = self.__select_identifier(arxiv=arxiv, doi=doi, isbn=isbn, issn=issn, pmid=pmid, scopus=scopus,
                                                 filehash=filehash)

        url = add_query_params('/catalog', {name: value, 'view': view})
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        if len(rsp.json()) == 0:
            raise MendeleyException('Catalog document not found')

        return view_type(view)(self.session, rsp.json()[0])

    def lookup(self, arxiv=None, doi=None, pmid=None, filehash=None, title=None, authors=None, year=None, source=None,
               view=None):
        url = add_query_params('/metadata', {'arxiv': arxiv, 'doi': doi, 'pmid': pmid, 'filehash': filehash,
                                             'title': title, 'authors': authors, 'year': year, 'source': source})
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        return LookupResponse(self.session, rsp.json(), view, view_type(view))

    def search(self, query, view=None):
        return CatalogSearch(self.session, query=query, view=view)

    @staticmethod
    def __select_identifier(**kwargs):
        identifiers = [(k, v) for k, v in iteritems(kwargs) if v]
        if (len(identifiers)) != 1:
            raise MendeleyException('Must specify exactly one identifier')

        return identifiers[0]


class CatalogSearch(ListResource):
    _content_type = 'application/vnd.mendeley-document.1+json'

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