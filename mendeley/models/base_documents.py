from mendeley.models.common import Person
from mendeley.response import SessionResponseObject


class BaseDocument(SessionResponseObject):
    content_type = 'application/vnd.mendeley-document.1+json'

    @property
    def authors(self):
        if 'authors' in self.json:
            return [Person(p) for p in self.json['authors']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'title', 'type', 'source', 'year', 'identifiers', 'keywords', 'abstract']


class BaseClientView(SessionResponseObject):
    @classmethod
    def fields(cls):
        return ['file_attached']


class BaseBibView(SessionResponseObject):
    @property
    def editors(self):
        if 'editors' in self.json:
            return [Person(p) for p in self.json['editors']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['pages', 'volume', 'issue', 'websites', 'month', 'publisher', 'day', 'city', 'edition', 'institution',
                'series', 'chapter', 'revision']
