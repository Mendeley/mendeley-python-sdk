from mendeley.models.documents import *
from mendeley.resources.base_documents import DocumentsBase


class Documents(DocumentsBase):
    _url = '/documents'

    def __init__(self, session, group_id):
        super(Documents, self).__init__(session, group_id)

    def create(self, title, type, **kwargs):
        kwargs['title'] = title
        kwargs['type'] = type
        kwargs['group_id'] = self.group_id

        kwargs = format_args(kwargs)
        content_type = UserDocument.content_type

        rsp = self.session.post(self._url, data=json.dumps(kwargs), headers={
            'Accept': content_type,
            'Content-Type': content_type
        })

        return UserAllDocument(self.session, rsp.json())

    @staticmethod
    def _view_type(view):
        return {
            'all': UserAllDocument,
            'bib': UserBibDocument,
            'client': UserClientDocument,
            'tags': UserTagsDocument,
            'core': UserDocument,
        }.get(view, UserDocument)
