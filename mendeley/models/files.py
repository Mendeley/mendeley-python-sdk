import json
import os
import re
from mendeley.models.annotations import Annotation

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
        """
        the URL at which the file can be downloaded.  This is only valid for a short time, so should not be cached.
        """
        file_url = '/files/%s' % self.id
        rsp = self.session.get(file_url, allow_redirects=False)
        return rsp.headers['location']

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

        with open(path, 'wb') as f:
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

    def add_sticky_note(self, text, x_position, y_position, page_number):
        """
        Adds a sticky note to this file.

        :param text: the text of the sticky_note.
        :param x_position: the x position on the file of the sticky_note.
        :param y_position: the y position on the file of the stick_note.
        :param page_number: the page_number on the file of the sticky_note.
        :return: a :class:`Annotation <mendeley.models.annotations.Annotation>`.
        """
        position = {'x': x_position, 'y': y_position}
        bounding_box = {'top_left': position, 'bottom_right': position, 'page': page_number}
        annotation = {
            'document_id': self.document().id,
            'text': text,
            'filehash': self.filehash,
            'positions': [bounding_box]
        }

        rsp = self.session.post('/annotations/', data=json.dumps(annotation), headers={
            'Accept': Annotation.content_type,
            'Content-Type': Annotation.content_type
        })

        return Annotation(self.session, rsp.json())

    def add_highlight(self, bounding_boxes, color):
        """
        Adds a highlight to this file.

        :param bounding_boxes: the area the highlight covers on the file.
        :param color: the color of the highlight.
        :return: a :class:`Annotation <mendeley.models.annotations.Annotation>`.
        """
        annotation = {
            'document_id': self.document().id,
            'filehash': self.filehash,
            'positions': [box.json for box in bounding_boxes],
            'color': color.json
        }

        rsp = self.session.post('/annotations/', data=json.dumps(annotation), headers={
            'Accept': Annotation.content_type,
            'Content-Type': Annotation.content_type
        })

        return Annotation(self.session, rsp.json())

    @classmethod
    def fields(cls):
        return ['id', 'size', 'file_name', 'mime_type', 'filehash']
