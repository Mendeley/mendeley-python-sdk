from mendeley.models.annotations import Annotation
from mendeley.resources.base import GetByIdResource, ListResource


class Annotations(GetByIdResource, ListResource):
    """
    Top-level resource for accessing annotations.
    """
    _url = '/annotations'

    def __init__(self, session):
        self.session = session

    def get(self, id):
        """
        Retrieves an annotation by ID.

        :param id: the ID of the annotation to get.
        :return: a :class:`Annotation <mendeley.models.annotations.Annotation>`.
        """
        return super(Annotations, self).get(id)

    def list(self, page_size=None, modified_since=None, deleted_since=None):
        """
        Retrieves annotations that the logged-in user is a member of, as a paginated collection.

        :param page_size: the number of annotations to return on each page.  Defaults to 20.
        :param modified_since: if specified, only returns files modified after this timestamp.
        :param deleted_since: if specified, only returns the IDs of documents deleted after this timestamp.
        :return: a :class:`Page <mendeley.pagination.Page>` of
        :class:`Annotations <mendeley.models.annotations.Annotation>`.
        """
        return super(Annotations, self).list(page_size, modified_since=modified_since, deleted_since=deleted_since)

    def iter(self, page_size=None, modified_since=None, deleted_since=None):
        """
        Retrieves annotations that the logged-in user is a member of, as an iterator.

        :param page_size: the number of annotations to retrieve at a time.  Defaults to 20.
        :param modified_since: if specified, only returns files modified after this timestamp.
        :param deleted_since: if specified, only returns the IDs of documents deleted after this timestamp.
        :return: an iterator of :class:`Annotations <mendeley.models.annotations.Annotation>`.
        """
        return super(Annotations, self).iter(page_size, modified_since=modified_since, deleted_since=deleted_since)

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return Annotation

