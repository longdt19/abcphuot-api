from api.common.base_resources import BaseResource

from .forms import *
from .business_logics import product_bl, category_bl


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


RESOURCES = {
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
