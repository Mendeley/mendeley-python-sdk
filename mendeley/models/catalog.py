from mendeley.models.base_documents import BaseDocument, BaseClientView, BaseBibView
from mendeley.response import LazyResponseObject


class CatalogDocument(BaseDocument):
    @classmethod
    def fields(cls):
        return super(CatalogDocument, cls).fields() + ['link']

    @property
    def files(self):
        return self.session.catalog_files(catalog_id=self.id)


class CatalogBibView(BaseBibView):
    pass


class CatalogClientView(BaseClientView):
    pass


class CatalogStatsView(object):
    @classmethod
    def fields(cls):
        return ['reader_count', 'reader_count_by_academic_status', 'reader_count_by_subdiscipline',
                'reader_count_by_country']


class CatalogBibDocument(CatalogBibView, CatalogDocument):
    @classmethod
    def fields(cls):
        return CatalogDocument.fields() + CatalogBibView.fields()


class CatalogClientDocument(CatalogClientView, CatalogDocument):
    @classmethod
    def fields(cls):
        return CatalogDocument.fields() + CatalogClientView.fields()


class CatalogStatsDocument(CatalogStatsView, CatalogDocument):
    @classmethod
    def fields(cls):
        return CatalogDocument.fields() + CatalogStatsView.fields()


class CatalogAllDocument(CatalogBibView, CatalogClientView, CatalogStatsView, CatalogDocument):
    @classmethod
    def fields(cls):
        return CatalogDocument.fields() + \
            CatalogBibView.fields() + \
            CatalogClientView.fields() + \
            CatalogStatsView.fields()


class LookupResponse(LazyResponseObject):
    def __init__(self, session, json, view, obj_type):
        super(LookupResponse, self).__init__(session, json['catalog_id'], obj_type, lambda: self._load())
        self.score = json['score']
        self.view = view

    def _load(self):
        return self.session.catalog.get(self.id, view=self.view)
