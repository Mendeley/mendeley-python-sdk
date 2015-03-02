import arrow
from mendeley.response import SessionResponseObject


class Annotation (SessionResponseObject):

    content_type = 'application/vnd.mendeley-annotation.1+json'

    def __init__(self, session, json):
        super(Annotation, self).__init__(session, json)

    @property
    def created(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def last_modified(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'last_modified' in self.json:
            return arrow.get(self.json['last_modified'])
        else:
            return None

    @property
    def profile(self):
        """
        a :class:`Profile <mendeley.models.profiles.Profile>`.
        """
        if 'profile_id' in self.json:
            return self.session.profiles.get_lazy(self.json['profile_id'])
        else:
            return None


    def document(self, view=None):
        """
        :param view: document view to return.
        :return: a :class:`UserDocument <mendeley.models.documents.UserDocument>`
        """
        if 'document_id' in self.json:
            return self.session.documents.get_lazy(self.json['document_id'], view=view)
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'text', 'privacy_level', 'note', 'type']