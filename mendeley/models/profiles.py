import arrow

from mendeley.models.common import Discipline, Photo, Location, Education, Employment
from mendeley.response import SessionResponseObject


class Profile(SessionResponseObject):
    """
    A Mendeley profile.

    .. attribute:: id
    .. attribute:: first_name
    .. attribute:: last_name
    .. attribute:: display_name
    .. attribute:: email
    .. attribute:: link
    .. attribute:: research_interests
    .. attribute:: academic_status
    .. attribute:: verified
    .. attribute:: user_type
    """
    content_type = 'application/vnd.mendeley-profiles.1+json'

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
    def discipline(self):
        """
        a :class:`Discipline <mendeley.models.common.Discipline>`.
        """
        if 'discipline' in self.json:
            return Discipline(self.json['discipline'])
        else:
            return None

    @property
    def photo(self):
        """
        a :class:`Photo <mendeley.models.common.Photo>`.
        """
        if 'photo' in self.json:
            return Photo(self.json['photo'])
        else:
            return None

    @property
    def location(self):
        """
        a :class:`Location <mendeley.models.common.Location>`.
        """
        if 'location' in self.json:
            return Location(self.json['location'])
        else:
            return None

    @property
    def education(self):
        """
        a list of :class:`Education <mendeley.models.common.Education>` objects.
        """
        if 'education' in self.json:
            return [Education(e) for e in self.json['education']]
        else:
            return None

    @property
    def employment(self):
        """
        a list of :class:`Employment <mendeley.models.common.Employment>` objects.
        """
        if 'employment' in self.json:
            return [Employment(e) for e in self.json['employment']]
        else:
            return None

    @classmethod
    def fields(cls):
        return ['id', 'first_name', 'last_name', 'display_name', 'email', 'link', 'research_interests',
                'academic_status', 'verified', 'user_type']
