import os
from slugify import slugify

from api.common.methods import get_now

from .constants import UPLOAD_DIR


class Uploader(object):

    def upload(self, file):
        filename = self._reformat_file_name(filename=file.filename)
        path = os.path.join(UPLOAD_DIR, filename)

        try:
            file.save(path)
        except Exception as error:
            raise error

        return path, os.path.getsize(path)

    def remove(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        except Exception as error:
            raise error

    def _reformat_file_name(self, filename):
        split_name = filename.split('.')
        ext = split_name.pop(len(split_name) - 1)
        return '%s__%s.%s' % (str(get_now()), slugify('.'.join(split_name)), ext)


uploader = Uploader()
