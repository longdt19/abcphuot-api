from api.common.base_forms import ValidationError, BaseCreateForm, BaseListForm, BaseReadForm, BaseUpdateForm, IdField, \
    fields, STRING_LENGTH_VALIDATORS, BaseForm, PhoneField

from .constants import ORDER_STATUSES


class OrderStatusField(fields.Field):
    def _validate(self, value):
        if value not in list(map(lambda item: item['id'], ORDER_STATUSES)):
            raise ValidationError('Invalid order status!')


class OrderCreatorForm(BaseForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    email = fields.Email(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    phone = PhoneField(required=True)
    address = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])


class OrderItemForm(BaseForm):
    product_id = IdField(required=True)
    count = fields.Integer(required=True, validate=lambda value: value > 0)
    metadata = fields.Dict(default={})


class CreateOrderForm(BaseCreateForm):
    order_items = fields.List(fields.Nested(OrderItemForm), required=True)
    order_creator = fields.Nested(OrderCreatorForm, required=True)
    description = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_LONG'])


class UpdateOrderForm(BaseUpdateForm):
    status = OrderStatusField()


class GetOrderForm(BaseReadForm):
    pass


class ListOrderForm(BaseListForm):
    search_text = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])

    total_min = fields.Integer()
    total_max = fields.Integer()
