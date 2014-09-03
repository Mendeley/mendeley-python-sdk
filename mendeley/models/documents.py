from mendeley.response import ResponseObject


class UserDocument(ResponseObject):
    content_type = 'application/vnd.mendeley-document.1+json'

    @classmethod
    def fields(cls):
        return ['id', 'title', 'type']

    def delete(self):
        self.session.documents.delete(self.id)
