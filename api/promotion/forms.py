from api.common.base_forms import ValidationError, BaseCreateForm, BaseListForm, BaseReadForm, BaseUpdateForm, IdField, \
    fields, STRING_LENGTH_VALIDATORS, BaseForm


class CreatePromotionPackageForm(BaseCreateForm):
    name = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    sale_off_value = fields.Integer(required=True, validate=lambda value: 0 <= value <= 100)


class UpdatePromotionPackageForm(BaseUpdateForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    sale_off_value = fields.Integer(validate=lambda value: 0 <= value <= 100)


class GetOnePromotionPackageForm(BaseReadForm):
    pass


class ListPromotionPackageForm(BaseListForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
