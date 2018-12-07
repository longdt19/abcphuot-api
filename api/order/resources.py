from api.common.base_resources import BaseResource

from .forms import *
from .business_logics import order_bl


class OrderResource(BaseResource):
    POST_INPUT_SCHEMA = CreateOrderForm()
    PATCH_INPUT_SCHEMA = UpdateOrderForm()
    GET_INPUT_SCHEMA = GetOrderForm()

    def post(self):
        params = self.parse_request_params()
        return order_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return order_bl.update(**params)

    def get(self):
        params = self.parse_request_params()
        return order_bl.get(**params)


class ListOrderResource(BaseResource):
    GET_INPUT_SCHEMA = ListOrderForm()

    def get(self):
        params = self.parse_request_params()
        return order_bl.list(**params)


RESOURCES = {
    '/order': {
        'resource': OrderResource,
        'required_auth_methods': ['PATCH', 'GET']
    },
    '/list-orders': {
        'resource': ListOrderResource,
        'required_auth_methods': ['GET']
    }
}
