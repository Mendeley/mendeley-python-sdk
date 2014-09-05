import os
import re

from mendeley.response import SessionResponseObject


class File(SessionResponseObject):
    """
    A file attached to a document.

    .. attribute:: id
    .. attribute:: size
    .. attribute:: file_name
    .. attribute:: mime_type
    .. attribute:: filehash
    .. attribute:: download_url
    """
    content_type = 'application/vnd.mendeley-file.1+json'
    filename_regex = re.compile('filename="(\S+)"')

    @property
    def download_url(self):
        return '%s/files/%s' % (self.session.host, self.id)

    def document(self, view=None):
        """
        :param view: document view to return.
        :return: a :class:`UserDocument <mendeley.models.documents.UserDocument>` or
                 :class:`CatalogDocument <mendeley.models.catalog.CatalogDocument>`, depending on which the document is
                 attached to.
        """
        if 'document_id' in self.json:
            return self.session.documents.get_lazy(self.json['document_id'], view=view)
        elif 'catalog_id' in self.json:
            return self.session.catalog.get_lazy(self.json['catalog_id'], view=view)
        else:
            return None

    def download(self, directory):
        """
        Downloads the file.

        :param directory: the directory to download the file to.  This must exist.
        :return: the path to the downloaded file.
        """
        rsp = self.session.get('/files/%s' % self.id, stream=True)
        filename = self.filename_regex.search(rsp.headers['content-disposition']).group(1)
        path = os.path.join(directory, filename)

        with open(path, 'w') as f:
            for block in rsp.iter_content(1024):
                if not block:
                    break

                f.write(block)

        return path

    def delete(self):
        """
        Deletes the file.
        """
        self.session.delete('/files/%s' % self.id)

    @classmethod
    def fields(cls):
        return ['id', 'size', 'file_name', 'mime_type', 'filehash']
