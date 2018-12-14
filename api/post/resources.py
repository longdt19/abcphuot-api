from api.common.base_resources import BaseResource

from .business_logics import banner_bl, post_bl, postblog_bl
from .forms import *


class BlogResource(BaseResource):
    POST_INPUT_SCHEMA = CreateBannerForm()
    PATCH_INPUT_SCHEMA = UpdateBannerForm()
    GET_INPUT_SCHEMA = GetBannerForm()

class BannerResource(BaseResource):
    POST_INPUT_SCHEMA = CreateBannerForm()
    PATCH_INPUT_SCHEMA = UpdateBannerForm()
    GET_INPUT_SCHEMA = GetBannerForm()

    def get(self):
        params = self.parse_request_params()
        return banner_bl.get(**params)

    def post(self):
        params = self.parse_request_params()
        return banner_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return banner_bl.update(**params)

    def delete(self):
        params = self.parse_request_params()
        return banner_bl.delete(**params)


class ListBannerResource(BaseResource):
    GET_INPUT_SCHEMA = ListBannerForm()

    def get(self):
        params = self.parse_request_params()
        return banner_bl.list(**params)


class ListPostResource(BaseResource):
    GET_INPUT_SCHEMA = ListPostForm()

    def get(self):
        params = self.parse_request_params()
        return post_bl.list(**params)


class PostResource(BaseResource):
    POST_INPUT_SCHEMA = CreatePostForm()
    PATCH_INPUT_SCHEMA = UpdatePostForm()
    GET_INPUT_SCHEMA = GetPostForm()

    def get(self):
        params = self.parse_request_params()
        return post_bl.get_one(**params)

    def post(self):
        params = self.parse_request_params()
        return post_bl.create(**params)

    def patch(self):
        params = self.parse_request_params()
        return post_bl.update(**params)

    def delete(self):
        params = self.parse_request_params()
        return post_bl.delete(**params)


RESOURCES = {
    '/banner': {
        'resource': BannerResource,
        'required_auth_methods': ['POST', 'PATCH', 'DELETE']
    },
    '/list-banners': {
        'resource': ListBannerResource
    },
    '/post': {
        'resource': PostResource,
    },
    '/list-posts': {
        'resource': ListPostResource
    }
}
