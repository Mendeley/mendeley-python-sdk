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
            return None

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
    .. attribute:: scopus_author_id
    """

    @classmethod
    def fields(cls):
        return ['first_name', 'last_name', 'scopus_author_id']

    @staticmethod
    def create(first_name, last_name, scopus_author_id):
        """
        Creates a person object, to be used when creating or updating a
        :class:`Document <mendeley.models.base_documents.BaseDocument>`.

        :param first_name:
        :param last_name:
        :param scopus_author_id:
        :return: a :class:`Person <mendeley.models.common.Person>`.
        """
        return Person({'first_name': first_name, 'last_name': last_name, 'scopus_author_id': scopus_author_id})


class Position(ResponseObject):
    """
    A position, associated with a :class:`Annotation <mendeley.models.annotations.Annotation>`.

    .. attribute:: x
    .. attribute:: y
    """
    @classmethod
    def fields(cls):
        return ['x', 'y']

    @staticmethod
    def create(x_position, y_position):
        """
        Creates a position object, to be used when creating or updating a
        :class:`Annotation <mendeley.models.annotations.Annotation>`.

        :param x_position:
        :param y_position:
        :return: a :class:`Position <mendeley.models.common.Position>`.
        """
        return Position({'x': x_position, 'y': y_position})


class BoundingBox(ResponseObject):
    """
    A bounding box, associated with a :class:`Annotation <mendeley.models.annotations.Annotation>`.

    .. attribute:: page
    """
    @classmethod
    def fields(cls):
        return ['page']

    @property
    def top_left(self):
        if 'top_left' in self.json:
            return Position.create(self.json['top_left']['x'], self.json['top_left']['y'])
        else:
            return None

    @property
    def bottom_right(self):
        if 'bottom_right' in self.json:
            return Position.create(self.json['bottom_right']['x'], self.json['bottom_right']['y'])
        else:
            return None

    @staticmethod
    def create(top_left, bottom_right, page):
        """
        Creates a bounding box object, to be used when creating or updating the
        :class:`Annotation <mendeley.models.annotations.Annotation>`.

        :param top_left:
        :param bottom_right:
        :param page:
        :return: a :class:`BoundingBox <mendeley.models.common.BoundingBox>`.
        """
        return BoundingBox({'top_left': top_left.json, 'bottom_right': bottom_right.json, 'page': page})


class Color(ResponseObject):
    """
    A color, associated with a :class:`Annotation <mendeley.models.annotations.Annotation>`.

    .. attribute:: r
    .. attribute:: g
    .. attribute:: b
    """
    @classmethod
    def fields(cls):
        return ['r', 'g', 'b']

    @staticmethod
    def create(red, green, blue):
        """
         Creates a color object, to be used when creating or updating a
        :class:`Annotation <mendeley.models.annotations.Annotation>`.

        :param red:
        :param green:
        :param blue:
        :return: a :class:`Color <mendeley.models.common.Color>`.
        """
        return Color({'r': red, 'g': green, 'b': blue})