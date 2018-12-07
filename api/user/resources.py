from api.common.base_resources import BaseResource

from .forms import *
from .business_logics import user_bl


class AuthResource(BaseResource):
    POST_INPUT_SCHEMA = AuthForm()

    def post(self):
        params = self.parse_request_params()
        return user_bl.authenticate(**params)


RESOURCES = {
    '/auth': {
        'resource': AuthResource
    }
}
