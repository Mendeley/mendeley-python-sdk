import arrow

from mendeley.response import ResponseObject


class Discipline(ResponseObject):
    """
    The discipline of a :class:`Profile <mendeley.models.profiles.Profile>`.

    .. attribute:: name
    .. attribute:: subdisciplines
    """
    @classmethod
    def fields(cls):
        return ['name', 'subdisciplines']


class Photo(ResponseObject):
    """
    A photo, associated with a :class:`Profile <mendeley.models.profiles.Profile>` or
    :class:`Group <mendeley.models.groups.Group>`.

    .. attribute:: original
    .. attribute:: standard
    .. attribute:: square
    """
    @classmethod
    def fields(cls):
        return ['original', 'standard', 'square']


class Location(ResponseObject):
    """
    A location, associated with a :class:`Profile <mendeley.models.profiles.Profile>`.

    .. attribute:: latitude
    .. attribute:: longitude
    .. attribute:: name
    """
    @classmethod
    def fields(cls):
        return ['latitude', 'longitude', 'name']


class Education(ResponseObject):
    """
    Education details, associated with a :class:`Profile <mendeley.models.profiles.Profile>`.

    .. attribute:: institution
    .. attribute:: degree
    .. attribute:: website
    """
    @property
    def start_date(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'start_date' in self.json:
            return arrow.get(self.json['start_date'])
        else:
            return

    @property
    def end_date(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'end_date' in self.json:
            return arrow.get(self.json['end_date'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['institution', 'degree', 'website']


class Employment(ResponseObject):
    """
    Employment details, associated with a :class:`Profile <mendeley.models.profiles.Profile>`.

    .. attribute:: institution
    .. attribute:: position
    .. attribute:: website
    .. attribute:: classes
    """
    @property
    def start_date(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'start_date' in self.json:
            return arrow.get(self.json['start_date'])
        else:
            return

    @property
    def end_date(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'end_date' in self.json:
            return arrow.get(self.json['end_date'])
        else:
            return None

    @classmethod
    def fields(cls):
        return ['institution', 'position', 'website', 'classes']


class Person(ResponseObject):
    """
    A person, associated with a :class:`Document <mendeley.models.base_documents.BaseDocument>`, as either an author
    or an editor.

    .. attribute:: first_name
    .. attribute:: last_name
    """
    @classmethod
    def fields(cls):
        return ['first_name', 'last_name']

    @staticmethod
    def create(first_name, last_name):
        """
        Creates a person object, to be used when creating or updating a
        :class:`Document <mendeley.models.base_documents.BaseDocument>`.

        :param first_name:
        :param last_name:
        :return: a :class:`Person <mendeley.models.common.Person>`.
        """
        return Person({'first_name': first_name, 'last_name': last_name})
