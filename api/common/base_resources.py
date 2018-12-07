from flask import request, abort
from flask_restful import Resource
from bson import json_util

from .base_errors import InvalidRequestParams
from .base_forms import BaseReadForm, BaseUpdateForm, BaseCreateForm, BaseDeleteForm


class BaseResource(Resource):
    POST_INPUT_SCHEMA = BaseCreateForm()
    PUT_INPUT_SCHEMA = BaseCreateForm()
    PATCH_INPUT_SCHEMA = BaseUpdateForm()
    GET_INPUT_SCHEMA = BaseReadForm()
    DELETE_INPUT_SCHEMA = BaseDeleteForm()

    POST_PARAM_LOCATION = 'json'
    PUT_PARAM_LOCATION = 'json'
    PATCH_PARAM_LOCATION = 'json'
    GET_PARAM_LOCATION = 'args'
    DELETE_PARAM_LOCATION = 'args'

    def parse_request_params(self):
        req_method = request.method
        input_schema = getattr(self, '%s_INPUT_SCHEMA' % req_method, None)

        param_location = getattr(self, '%s_PARAM_LOCATION' % req_method, None)
        if not param_location:
            return abort(405)

        raw_params = getattr(request, param_location) or {}
        if req_method == 'GET':
            try:
                raw_params = json_util.loads(raw_params.get('params') or '{}')
            except Exception:
                raise InvalidRequestParams(payload=raw_params)

        if not input_schema:
            return raw_params

        errors = input_schema.validate(raw_params)
        if errors:
            raise InvalidRequestParams(message=errors)

        return input_schema.dump(raw_params).data
