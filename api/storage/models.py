from api.common.base_models import BaseDocument, db, STRING_LENGTH

from .uploaders import uploader


class File(object):
    url = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
    path = db.StringField(max_length=STRING_LENGTH['LONG'], required=True, unique=True)
    name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)

    size = db.IntField(required=True)

    def delete(self, *args, **kwargs):
        uploader.remove(path=self.path)
        return super().delete(*args, **kwargs)


class Image(File, BaseDocument):
    # object_type = db.StringField(required=True, max_length=STRING_LENGTH['EX_SHORT'])
    # object_id = db.ObjectIdField(required=True)
    pass
