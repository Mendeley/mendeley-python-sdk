import json
import arrow
from mendeley.models.common import BoundingBox, Color
from mendeley.response import SessionResponseObject


class Annotation (SessionResponseObject):

    content_type = 'application/vnd.mendeley-annotation.1+json'

    def __init__(self, session, json):
        super(Annotation, self).__init__(session, json)

    def update(self, **kwargs):
        """
        Updates this annotation.

        """

        rsp = self.session.patch('/annotations/%s' % self.id, data=json.dumps(format_args(kwargs)), headers={
            'Accept': self.content_type,
            'Content-Type': self.content_type
        })

        return Annotation(self.session, rsp.json())

    def delete(self):
        """
        Permanently deletes this annotation.
        """
        self.session.delete('/annotations/%s' % self.id)

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

    @property
    def positions(self):
        """
        a list of :class:`BoundingBox <mendeley.models.common.BoundingBox>`.
        """
        if 'positions' in self.json:
            return [BoundingBox(p) for p in self.json['positions']]
        else:
            return None

    @property
    def color(self):
        """
        a :class:`Color <mendeley.models.common.Color>`.
        """
        if 'color' in self.json:
            return Color(self.json['color'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'text', 'privacy_level', 'note', 'type']


def format_args(kwargs):
    if 'positions' in kwargs:
        kwargs['positions'] = [box.json for box in kwargs['positions']]

    if 'color' in kwargs:
        kwargs['color'] = kwargs['color'].json

    return kwargs