from api.common.base_resources import BaseResource

from .forms import *
from .business_logics import order_bl, simorder_bl


class OrderResource(BaseResource):
    POST_INPUT_SCHEMA = CreateOrderForm()
    GET_INPUT_SCHEMA = ListSimOrderForm()

    def get(self):
        print ('get1')
        params = self.parse_request_params()
        print ('get2', params)
        return order_bl.list(**params)

    def post(self):
        params = self.parse_request_params()
        return order_bl.create(**params)

class SimOrderResource(BaseResource):
    GET_INPUT_SCHEMA = ListSimOrderForm()

    def get(self):
        params = self.parse_request_params()
        return simorder_bl.list(**params)

RESOURCES = {
    '/order': {
        'resource': OrderResource
    }
}
