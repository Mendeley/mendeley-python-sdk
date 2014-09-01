from future.utils import iteritems

from mendeley.exception import MendeleyException
from mendeley.models.catalog import *
from mendeley.resources.base import add_query_params


class Catalog(object):
    _content_type = 'application/vnd.mendeley-document.1+json'

    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        url = add_query_params('/catalog/%s' % id, {'view': view})
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        return self.__view_type(view)(self.session, rsp.json())

    def by_identifier(self, arxiv=None, doi=None, isbn=None, issn=None, pmid=None, scopus=None, filehash=None,
                      view=None):
        (name, value) = self.__select_identifier(arxiv=arxiv, doi=doi, isbn=isbn, issn=issn, pmid=pmid, scopus=scopus,
                                                 filehash=filehash)

        url = add_query_params('/catalog', {name: value, 'view': view})
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        if len(rsp.json()) == 0:
            raise MendeleyException('Catalog document not found')

        return self.__view_type(view)(self.session, rsp.json()[0])

    def lookup(self, arxiv=None, doi=None, pmid=None, filehash=None, title=None, authors=None, year=None, source=None,
               view=None):
        url = add_query_params('/metadata', {'arxiv': arxiv, 'doi': doi, 'pmid': pmid, 'filehash': filehash,
                                             'title': title, 'authors': authors, 'year': year, 'source': source})
        rsp = self.session.get(url, headers={'Accept': self._content_type})

        return LookupResponse(self.session, rsp.json(), view, self.__view_type(view))

    @staticmethod
    def __view_type(view):
        return {
            'bib': CatalogBibDocument,
            'client': CatalogClientDocument,
            'stats': CatalogStatsDocument,
            'all': CatalogAllDocument,
            'core': CatalogCoreDocument
        }.get(view, CatalogCoreDocument)

    @staticmethod
    def __select_identifier(**kwargs):
        identifiers = [(k, v) for k, v in iteritems(kwargs) if v]
        if (len(identifiers)) != 1:
            raise MendeleyException('Must specify exactly one identifier')

        return identifiers[0]
