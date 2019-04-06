import arrow

from mendeley.models.common import Photo
from mendeley.models.profiles import Profile
from mendeley.response import SessionResponseObject, LazyResponseObject


class Group(SessionResponseObject):
    """
    A Mendeley group.

    .. attribute:: id
    .. attribute:: name
    .. attribute:: description
    .. attribute:: disciplines
    .. attribute:: tags
    .. attribute:: webpage
    .. attribute:: link
    .. attribute:: access_level
    .. attribute:: role
    """
    content_type = 'application/vnd.mendeley-group.1+json'

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
    def photo(self):
        """
        a :class:`Photo <mendeley.models.common.Photo>`.
        """
        if 'photo' in self.json:
            return Photo(self.json['photo'])
        else:
            return None

    @property
    def owner(self):
        """
        a :class:`Profile <mendeley.models.profiles.Profile>`.
        """
        if 'owning_profile_id' in self.json:
            return self.session.profiles.get_lazy(self.json['owning_profile_id'])
        else:
            return None

    @property
    def members(self):
        return self.session.group_members(self.id)

    @property
    def folders(self):
        return self.session.group_folders(self.id)

    @property
    def documents(self):
        """
        a :class:`Documents <mendeley.resources.documents.Documents>` resource, from which
        :class:`UserDocuments <mendeley.models.documents.UserDocument>` can be retrieved.
        """
        return self.session.group_documents(self.id)

    @property
    def trash(self):
        """
        a :class:`Trash <mendeley.resources.trash.Trash>` resource, from which
        :class:`TrashDocuments <mendeley.models.documents.TrashDocument>` can be retrieved.
        """
        return self.session.group_trash(self.id)

    @property
    def files(self):
        """
        a :class:`Files <mendeley.resources.files.Files>` resource, from which
        :class:`Files <mendeley.models.files.File>` can be retrieved.
        """
        return self.session.group_files(self.id)

    @classmethod
    def fields(cls):
        return ['id', 'name', 'description', 'disciplines', 'tags', 'webpage', 'link', 'access_level',
                'role']


class GroupMember(LazyResponseObject, Profile):
    """
    A member of a Mendeley group.

    .. attribute:: id
    .. attribute:: role
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
    content_type = 'application/vnd.mendeley-membership.1+json'

    def __init__(self, session, member_json):
        super(GroupMember, self).__init__(session, member_json.get('profile_id'), Profile, lambda: self._load())

        self.member_json = member_json

    @property
    def joined(self):
        """
        an :class:`Arrow <arrow.arrow.Arrow>` object.
        """
        if 'joined' in self.member_json:
            return arrow.get(self.member_json['joined'])
        else:
            return None

    @property
    def role(self):
        return self.member_json.get('role')

    def _load(self):
        return self.session.profiles.get(self.id)
