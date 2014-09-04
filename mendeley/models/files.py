import os
import re

from mendeley.response import SessionResponseObject


class File(SessionResponseObject):
    content_type = 'application/vnd.mendeley-file.1+json'
    filename_regex = re.compile('filename="(\S+)"')

    @property
    def download_url(self):
        return '%s/files/%s' % (self.session.host, self.id)

    @classmethod
    def fields(cls):
        return ['id', 'size', 'file_name', 'mime_type', 'filehash']

    def download(self, directory):
        rsp = self.session.get('/files/%s' % self.id, stream=True)
        filename = self.filename_regex.search(rsp.headers['content-disposition']).group(1)
        path = os.path.join(directory, filename)

        with open(path, 'w') as f:
            for block in rsp.iter_content(1024):
                if not block:
                    break

                f.write(block)

        return path
