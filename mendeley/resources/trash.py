from mendeley.models.documents import TrashAllDocument, TrashBibDocument, TrashClientDocument, TrashTagsDocument, \
    TrashDocument
from mendeley.resources.base import add_query_params
from mendeley.resources.base_documents import DocumentsBase


class Trash(DocumentsBase):
    _url = '/trash'

    def __init__(self, session, group_id):
        super(Trash, self).__init__(session, group_id)

    def get(self, id, view=None):
        url = add_query_params('%s/%s' % (self._url, id), {'view': view})
        obj_type = self._view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        return obj_type(self.session, rsp.json())

    def restore(self, id):
        url = '%s/%s/restore' % (self._url, id)
        self.session.post(url)

    @staticmethod
    def _view_type(view):
        return {
            'all': TrashAllDocument,
            'bib': TrashBibDocument,
            'client': TrashClientDocument,
            'tags': TrashTagsDocument,
            'core': TrashDocument,
        }.get(view, TrashDocument)
