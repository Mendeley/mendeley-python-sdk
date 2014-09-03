from mendeley.models.documents import TrashAllDocument, TrashBibDocument, TrashClientDocument, TrashTagsDocument, \
    TrashDocument
from mendeley.resources.base_documents import DocumentsBase


class Trash(DocumentsBase):
    _url = '/trash'

    def __init__(self, session, group_id):
        super(Trash, self).__init__(session, group_id)

    @staticmethod
    def _view_type(view):
        return {
            'all': TrashAllDocument,
            'bib': TrashBibDocument,
            'client': TrashClientDocument,
            'tags': TrashTagsDocument,
            'core': TrashDocument,
        }.get(view, TrashDocument)
