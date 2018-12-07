from api.common.base_resources import BaseResource

from .business_logics import entrance_bl


class EntranceResource(BaseResource):
    def get(self):
        return entrance_bl.get_constants()


RESOURCES = {
    '/constants': {
        'resource': EntranceResource
    }
}
