import arrow
import json
from mendeley.response import SessionResponseObject, LazyResponseObject

class Folder(SessionResponseObject):
    """
    A Mendeley folder.

    .. attribute:: id
    .. attribute:: name
    .. attribute:: created
    .. attribute:: modified
    .. attribute:: parent_id
    .. attribute:: group_id
    """
    content_type = 'application/vnd.mendeley-folder.1+json'

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
            return arrow.get(self.json['modified'])
        elif 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def group(self):
        """
        a :class:`Group <mendeley.models.groups.Group>`.
        """
        if 'group_id' in self.json:
            return self.session.groups.get_lazy(self.json['group_id'])
        else:
            return None

    @property
    def parent(self):
        if 'parent_id' in self.json:
            return self.session.folders.get_lazy(self.json['parent_id'])
        else:
            return None

    @property
    def documents(self):
        """
        a :class:`Documents <mendeley.resources.documents.Documents>` resource, from which
        :class:`UserDocuments <mendeley.models.documents.UserDocument>` can be retrieved.
        """
        return self.session.folder_documents(folder_id=self.id, group_id=self.group_id)

    @property
    def files(self):
        """
        a :class:`Files <mendeley.resources.files.Files>` resource, from which
        :class:`Files <mendeley.models.files.File>` can be retrieved.
        """
        return self.session.group_files(self.id)

    def create(self, name):
        """
        Creates a new folder that is a subfolder of the current folder

        :param name: name of the folder.
        :return: a :class:`Folder <mendeley.models.folders.Folder>`.
        """
        return self.session.group_folders(self.group_id).create(name, parent_id=self.id)

    def delete(self):
        """
        Permanently deletes this folder and any subfolders
        """
        self.session.delete('/folders/%s' % self.id)

    def add_document(self, doc):

        data = {'id':doc.id}
        self.session.post('/folders/{}/documents'.format(self.id), data=json.dumps(data), headers={
            'Accept': doc.content_type,
            'Content-Type': doc.content_type
        } )

    def remove_document(self, doc):
        self.session.delete('/folders/{}/documents/{}'.format(self.id, doc.id))

    @classmethod
    def fields(cls):
        return ["id", "name", "created", "modified", "parent_id", "group_id"]


