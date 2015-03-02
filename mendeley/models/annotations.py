from mendeley.response import SessionResponseObject


class Annotation (SessionResponseObject):

    content_type = 'application/vnd.mendeley-annotation.1+json'

    def __init__(self, session, json):
        super(Annotation, self).__init__(session, json)


    @classmethod
    def fields(cls):
        return ['id', 'text']