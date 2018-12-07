from api.common.base_models import BaseDocument, db, STRING_LENGTH


class PromotionPackage(BaseDocument):
    name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)

    sale_off_value = db.IntField(required=True)
