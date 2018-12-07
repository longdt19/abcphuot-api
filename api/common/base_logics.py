from slugify import slugify

from .methods import get_now
from .base_errors import InvalidRequestParams, PermissionError


class BaseLogic(object):
    def _get_slug_with_datetime(self, string):
        string_datetime = str(get_now()).replace('.', '')
        return slugify(string) + '-' + string_datetime

    def _get_record_by_id(self, model, id, get_query=False):
        query = model.objects(id=id)
        if not query.count(True):
            raise InvalidRequestParams('%s not found!' % model.__name__, payload=id)
        if get_query:
            return query
        return query.first()

    def _get_object(self, object_id, object_type, type_map):
        try:
            object_model = type_map[object_type]
        except KeyError:
            raise InvalidRequestParams('Invalid object_type!')
        return self._get_record_by_id(model=object_model, id=object_id)
