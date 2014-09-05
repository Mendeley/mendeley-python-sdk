from mendeley.models.base_documents import BaseDocument, BaseClientView, BaseBibView
from mendeley.response import LazyResponseObject


class CatalogDocument(BaseDocument):
    """
    Base class for catalog documents.

    .. attribute:: id
    .. attribute:: title
    .. attribute:: type
    .. attribute:: source
    .. attribute:: year
    .. attribute:: identifiers
    .. attribute:: keywords
    .. attribute:: abstract
    .. attribute:: link
    """
    @property
    def files(self):
        """
        a :class:`Files <mendeley.resources.files.Files>` resource, from which
        :class:`Files <mendeley.models.files.File>` can be retrieved.
        """
        return self.session.catalog_files(catalog_id=self.id)

    @classmethod
    def fields(cls):
        return super(CatalogDocument, cls).fields() + ['link']


class CatalogBibView(BaseBibView):
    """
    Additional fields returned when getting a :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>` with
    view='bib' or 'all'.

    .. attribute:: pages
    .. attribute:: volume
    .. attribute:: issue
    .. attribute:: websites
    .. attribute:: month
    .. attribute:: publisher
    .. attribute:: day
    .. attribute:: city
    .. attribute:: edition
    .. attribute:: institution
    .. attribute:: series
    .. attribute:: chapter
    .. attribute:: revision
    """
    pass


class CatalogClientView(BaseClientView):
    """
    Additional fields returned when getting a :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>` with
    view='client' or 'all'.

    .. attribute:: file_attached
    """
    pass


class CatalogStatsView(object):
    """
    Additional fields returned when getting a :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>` with
    view='stats' or 'all'.

    .. attribute:: reader_count
    .. attribute:: reader_count_by_academic_status
    .. attribute:: reader_count_by_subdiscipline
    .. attribute:: reader_count_by_country
    """
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
