from api.common.base_models import BaseDocument, db, STRING_LENGTH, SimpleEmbeddedDocument


class Order(BaseDocument):
    product_id = db.ObjectIdField(required=True)
    quantity = db.IntField(required=True)
    name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
    email = db.StringField(max_length=STRING_LENGTH['LONG'])
    phone = db.StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
    description = db.StringField(max_length=STRING_LENGTH['EX_SHORT'])
    address = db.StringField(max_length=STRING_LENGTH['EX_LONG'])
    product_type = db.StringField(max_length=STRING_LENGTH['LONG'])
    status = db.IntField(required=True)

# class OrderItem(SimpleEmbeddedDocument):
#     product_id = db.ObjectIdField(required=True)
#     product_category = db.ObjectIdField(required=True)
#
#     discount_package_id = db.ObjectIdField()
#
#     product_name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
#     product_slug = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
#     product_image_url = db.StringField(max_length=STRING_LENGTH['LONG'])
#     product_price = db.IntField(required=True)
#     discount_package_value = db.IntField()
#
#     count = db.IntField(required=True)
#     total = db.IntField(required=True)
#
#     metadata = db.DictField()
#
#
# class OrderCreator(SimpleEmbeddedDocument):
#     name = db.StringField(max_length=STRING_LENGTH['LONG'])
#     slug = db.StringField(max_length=STRING_LENGTH['LONG'])
#     email = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
#     phone = db.StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
#     ip = db.StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
#     address = db.StringField(max_length=STRING_LENGTH['EX_LONG'])
#
#
# class Order(BaseDocument):
#     status = db.StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
#     description = db.StringField(max_length=STRING_LENGTH['EX_LONG'])
#
#     items = db.ListField(db.EmbeddedDocumentField(OrderItem), required=True)
#
#     creator_info = db.EmbeddedDocumentField(OrderCreator, required=True)
#
#     total = db.IntField(required=True)
