from slugify import slugify

from api.common.base_logics import BaseLogic

from .models import PromotionPackage
from .errors import *


class PromotionPackageBL(BaseLogic):

    def _is_name_duplicate(self, name, id=None):
        params = dict(
            slug=slugify(name)
        )
        if id:
            params['id__ne'] = id

        matched = PromotionPackage.objects(**params).first()
        return matched is not None

    def get(self, id):
        package = self._get_record_by_id(id=id, model=PromotionPackage)
        result = package.output()
        return result

    def create(self, name, sale_off_value):
        package = PromotionPackage()
        if self._is_name_duplicate(name=name):
            raise NameAlreadyExists

        package.name = name
        package.sale_off_value = sale_off_value

        package.create()
        return package.output()

    def update(self, id, name=None, sale_off_value=None):

        package = self._get_record_by_id(model=PromotionPackage, id=id)

        update_params = dict()

        if name:
            if self._is_name_duplicate(name=name, id=id):
                raise NameAlreadyExists
            update_params['name'] = name

        if sale_off_value is not None:
            update_params['sale_off_value'] = sale_off_value

        if update_params:
            package.patch(update_params=update_params)

        return dict(success=True)

    def list(self, page, per_page, order, name=None):
        params = dict()
        if name:
            params['slug__contains'] = slugify(name)

        matches = PromotionPackage.objects(**params)
        matches = matches.order_by(order)
        total = matches.count(True)

        result = []

        for record in matches.paginate(page=page, per_page=per_page).items:
            record_output = record.output()
            result.append(record_output)

        return dict(total=total, result=result)


promotion_package_bl = PromotionPackageBL()
