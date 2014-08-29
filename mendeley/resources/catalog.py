from future.utils import iteritems

from mendeley.exception import MendeleyException
from mendeley.models import Person
from mendeley.resources.base import add_query_params
from mendeley.response import ResponseObject, LazyResponseObject


class Catalog(object):
    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        url = add_query_params('/catalog/%s' % id, {'view': view})
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-document.1+json'})

        return self.__view_type(view)(self.session, rsp.json())

    def by_identifier(self, arxiv=None, doi=None, isbn=None, issn=None, pmid=None, scopus=None, filehash=None,
                      view=None):
        (name, value) = self.__select_identifier(arxiv=arxiv, doi=doi, isbn=isbn, issn=issn, pmid=pmid, scopus=scopus,
                                                 filehash=filehash)

        url = add_query_params('/catalog', {name: value, 'view': view})
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-document.1+json'})

        if len(rsp.json()) == 0:
            raise MendeleyException('Catalog document not found')

        return self.__view_type(view)(self.session, rsp.json()[0])

    def lookup(self, arxiv=None, doi=None, pmid=None, filehash=None, title=None, authors=None, year=None, source=None,
               view=None):
        url = add_query_params('/metadata', {'arxiv': arxiv, 'doi': doi, 'pmid': pmid, 'filehash': filehash,
                                             'title': title, 'authors': authors, 'year': year, 'source': source})
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-document-lookup.1+json'})

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


class CatalogCoreDocument(ResponseObject):
    @property
    def authors(self):
        if 'authors' in self._json:
            return [Person(self.session, p) for p in self._json['authors']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'title', 'type', 'source', 'year', 'identifiers', 'link', 'keywords', 'abstract']


class CatalogBibView(ResponseObject):
    @property
    def editors(self):
        if 'editors' in self._json:
            return [Person(self.session, p) for p in self._json['editors']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['pages', 'volume', 'issue', 'websites', 'month', 'publisher', 'day', 'city', 'edition', 'institution',
                'series', 'chapter', 'revision']


class CatalogClientView(ResponseObject):
    @classmethod
    def fields(cls):
        return ['file_attached']


class CatalogStatsView(ResponseObject):
    @classmethod
    def fields(cls):
        return ['reader_count', 'reader_count_by_academic_status', 'reader_count_by_subdiscipline',
                'reader_count_by_country']


class CatalogBibDocument(CatalogBibView, CatalogCoreDocument):
    @classmethod
    def fields(cls):
        return CatalogCoreDocument.fields() + CatalogBibView.fields()


class CatalogClientDocument(CatalogClientView, CatalogCoreDocument):
    @classmethod
    def fields(cls):
        return CatalogCoreDocument.fields() + CatalogClientView.fields()


class CatalogStatsDocument(CatalogStatsView, CatalogCoreDocument):
    @classmethod
    def fields(cls):
        return CatalogCoreDocument.fields() + CatalogStatsView.fields()


class CatalogAllDocument(CatalogBibView, CatalogClientView, CatalogStatsView, CatalogCoreDocument):
    @classmethod
    def fields(cls):
        return CatalogCoreDocument.fields() + \
            CatalogBibView.fields() + \
            CatalogClientView.fields() + \
            CatalogStatsView.fields()


class LookupResponse(LazyResponseObject):
    def __init__(self, session, json, view, obj_type):
        super(LookupResponse, self).__init__(session, json['catalog_id'], obj_type)
        self.score = json['score']
        self.view = view

    def _load(self):
        url = add_query_params('/catalog/%s' % self.id, {'view': self.view})
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-document.1+json'})

        return rsp.json()
