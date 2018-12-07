from api.common.base_forms import ValidationError, BaseCreateForm, BaseListForm, BaseReadForm, BaseUpdateForm, IdField, \
    fields, STRING_LENGTH_VALIDATORS, BaseForm

from .models import Category
from .constants import PRODUCT_STATUSES, PRODUCT_SIZES


class CategoryField(IdField):
    def _validate(self, value):
        super()._validate(value=value)
        if not Category.objects(id=value).first():
            raise ValidationError('Invalid category id!')


class ProductStatusField(fields.Field):
    def _validate(self, value):
        if value not in list(map(lambda item: item['id'], PRODUCT_STATUSES)):
            raise ValidationError('Invalid product status!')


class ProductSizeField(fields.Field):
    def _validate(self, value):
        if value not in list(map(lambda item: item['id'], PRODUCT_SIZES)):
            raise ValidationError('Invalid product size!')


class CreateCategoryForm(BaseCreateForm):
    name = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    parent_id = CategoryField()


class UpdateCategoryForm(BaseUpdateForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    parent_id = IdField()


class GetCategoryForm(BaseReadForm):
    pass


class ListCategoryForm(BaseListForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])

    parent_id = IdField()

    get_parents = fields.Boolean()


class CreateProductForm(BaseCreateForm):
    name = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    code = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_SHORT'])

    price = fields.Integer()

    category_id = CategoryField(required=True)

    status = ProductStatusField()

    sizes = fields.List(ProductSizeField())

    promotion_package_id = IdField(allow_none=True)


class UpdateProductForm(BaseUpdateForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    code = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_SHORT'])

    price = fields.Integer()

    default_image_id = IdField()

    status = ProductStatusField()

    sizes = fields.List(ProductSizeField())

    promotion_package_id = IdField(allow_none=True)


class ListProductForm(BaseListForm):
    search_text = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])

    categories = fields.List(IdField())

    statuses = fields.List(ProductStatusField())

    is_sale_off = fields.Boolean()


class GetProductForm(BaseForm):
    slug = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    id = IdField()
