from api.common.base_resources import BaseResource

from .forms import *
from .business_logics import promotion_package_bl


class PromotionPackageResource(BaseResource):
    POST_INPUT_SCHEMA = CreatePromotionPackageForm()
    PATCH_INPUT_SCHEMA = UpdatePromotionPackageForm()
    GET_INPUT_SCHEMA = GetOnePromotionPackageForm()

    def post(self):
        params = self.parse_request_params()
        return promotion_package_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return promotion_package_bl.update(**params)

    def get(self):
        params = self.parse_request_params()
        return promotion_package_bl.get(**params)


class ListPromotionPackageResource(BaseResource):
    GET_INPUT_SCHEMA = ListPromotionPackageForm()

    def get(self):
        params = self.parse_request_params()
        return promotion_package_bl.list(**params)


RESOURCES = {
    '/promotion-package': {
        'resource': PromotionPackageResource,
        'required_auth_methods': ['POST', 'PATCH', 'GET']
    },
    '/promotion-package-list': {
        'resource': ListPromotionPackageResource,
        'required_auth_methods': ['GET']
    }
}
