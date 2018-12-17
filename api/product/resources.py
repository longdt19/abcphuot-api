from api.common.base_resources import BaseResource

from .forms import *
from .business_logics import product_bl, category_bl, sim_bl, wifi_bl


class WifiProductResource(BaseResource):
    GET_INPUT_SCHEMA = ListWifiProductForm()
    POST_INPUT_SCHEMA = CreateWifiForm()
    PATCH_INPUT_SCHEMA = UpdateWifiForm()

    def get(self):
        params = self.parse_request_params()
        return wifi_bl.list(**params)

    def post(self):
        params = self.parse_request_params()
        return wifi_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return wifi_bl.update(**params)

    def delete(self):
        params = self.parse_request_params()
        return wifi_bl.delete(**params)

class SimProductResource(BaseResource):
    GET_INPUT_SCHEMA = ListSimProductForm()
    POST_INPUT_SCHEMA = CreateSimForm()
    PATCH_INPUT_SCHEMA = UpdateSimForm()

    def get(self):
        params = self.parse_request_params()
        return sim_bl.list(**params)

    def post(self):
        params = self.parse_request_params()
        return sim_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return sim_bl.update(**params)

    def delete(self):
        params = self.parse_request_params()
        return sim_bl.delete(**params)

class ProductResource(BaseResource):
    POST_INPUT_SCHEMA = CreateProductForm()
    PATCH_INPUT_SCHEMA = UpdateProductForm()
    GET_INPUT_SCHEMA = GetProductForm()

    def post(self):
        params = self.parse_request_params()
        return product_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return product_bl.update(**params)

    def get(self):
        params = self.parse_request_params()
        return product_bl.get(**params)


class ListProductResource(BaseResource):
    GET_INPUT_SCHEMA = ListProductForm()

    def get(self):
        params = self.parse_request_params()
        return product_bl.list(**params)


class ListProductCategoryResource(BaseResource):
    GET_INPUT_SCHEMA = ListCategoryForm()

    def get(self):
        params = self.parse_request_params()
        return category_bl.list(**params)


class CategoryResource(BaseResource):
    POST_INPUT_SCHEMA = CreateCategoryForm()
    PATCH_INPUT_SCHEMA = UpdateCategoryForm()
    GET_INPUT_SCHEMA = GetCategoryForm()

    def post(self):
        params = self.parse_request_params()
        return category_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return category_bl.update(**params)

    def get(self):
        params = self.parse_request_params()
        return category_bl.get_one(**params)

    def delete(self):
        params = self.parse_request_params()
        return category_bl.delete(**params)


class GetSimResource(BaseResource):
    POST_INPUT_SCHEMA = GetSimForm()

    def post(self):
        params = self.parse_request_params()
        return sim_bl.get_one(**params)

class GetWifiResource(BaseResource):
    POST_INPUT_SCHEMA = GetWifiForm()

    def post(self):
        params = self.parse_request_params()
        return wifi_bl.get_one(**params)


RESOURCES = {
    '/get-sim': {
        'resource': GetSimResource
    },
    '/get-wifi': {
        'resource': GetWifiResource
    },
    '/sim-product': {
        'resource': SimProductResource
    },
    '/wifi-product': {
        'resource': WifiProductResource
    },
    '/product': {
        'resource': ProductResource,
        'required_auth_methods': ['POST', 'PATCH']
    },
    '/list-products': {
        'resource': ListProductResource,
    },
    '/list-product-categories': {
        'resource': ListProductCategoryResource,
    },
    '/product-category': {
        'resource': CategoryResource,
        'required_auth_methods': ['POST', 'DELETE', 'PATCH']
    }
}
