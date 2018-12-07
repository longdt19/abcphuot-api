from api.common.base_models import BaseDocument, db, STRING_LENGTH

class Category(BaseDocument):
    name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
    parent_id = db.ObjectIdField()
    images = db.ListField(db.ObjectIdField(), default=[])


class Product(BaseDocument):

    name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)
    status = db.StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
    code = db.StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True, unique=True)

    price = db.IntField(default=0)

    promotion_package_id = db.ObjectIdField(null=True)
    category_id = db.ObjectIdField(required=True)

    images = db.ListField(db.ObjectIdField(), default=[])
    default_image_id = db.ObjectIdField()

    sizes = db.ListField(db.StringField(max_length=STRING_LENGTH['EX_SHORT']), default=[])

    def make_product_code(self, category_slug):
        split_name = category_slug.split('-')

        prefix = ''
        for word in split_name:
            prefix += word[0].upper()

        code = prefix + str(Product.objects.count())

        if Product.objects(code=code).first():
            return self.make_product_code(category_slug)

        self.code = code
