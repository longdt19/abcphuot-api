from api.common.base_models import BaseDocument, db, STRING_LENGTH

#
# class PostBlog(BaseDocument):
#     #  Kinh nghiệm, Cảm nhận,  Địa điểm
#     category_id = db.StringField(required=True, max_length=STRING_LENGTH['EX_SHORT'])
#     content = db.StringField(max_length=STRING_LENGTH['EX_LARGE'])
#     images = db.ListField(db.ObjectIdField(), default=[])
#     title = db.StringField(required=True, max_length=STRING_LENGTH['LONG'])


class Banner(BaseDocument):
    name = db.StringField(required=True, max_length=STRING_LENGTH['LONG'])

    object_type = db.StringField(max_length=STRING_LENGTH['EX_SHORT'])

    images = db.ListField(db.ObjectIdField(), default=[])


class Post(BaseDocument):
    category_id = db.StringField(required=True, max_length=STRING_LENGTH['EX_SHORT'])
    name = db.StringField(required=True, max_length=STRING_LENGTH['LONG'])
    content = db.StringField(max_length=STRING_LENGTH['EX_LARGE'])
    images = db.ListField(db.ObjectIdField(), default=[])
    banner = db.ObjectIdField()
