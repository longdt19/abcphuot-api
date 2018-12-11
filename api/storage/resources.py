from flask import request

from api.common.base_resources import BaseResource
from api.common.base_errors import InvalidRequestParams

from .forms import *
from .business_logics import image_bl, storage_bl


class ImageResource(BaseResource):
    POST_INPUT_SCHEMA = CreateImageForm()
    POST_PARAM_LOCATION = 'form'

    GET_INPUT_SCHEMA = ListImageForm()

    def post(self):
        file = request.files.get('file')
        if not file:
            raise InvalidRequestParams('Missing file!')

        params = self.parse_request_params()
        return image_bl.create(file=file, **params)

    def get(self):
        params = self.parse_request_params()
        return image_bl.list(**params)

    def delete(self):
        params = self.parse_request_params()
        return image_bl.delete(**params)


class DownloadResource(BaseResource):
    GET_INPUT_SCHEMA = DownloadFileForm()

    def get(self):
        params = self.parse_request_params()
        return storage_bl.download(**params)


RESOURCES = {
    '/image': {
        'resource': ImageResource,
    },
    '/download': {
        'resource': DownloadResource
    }
}
