from mendeley.models.common import Person
from mendeley.resources.base import add_query_params
from mendeley.response import ResponseObject, LazyResponseObject


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
