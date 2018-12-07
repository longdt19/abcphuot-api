from slugify import slugify
from mongoengine import Q

from api.common.base_logics import BaseLogic
from api.common.base_errors import InvalidRequestParams, PermissionError
from api.storage.models import Image
from api.promotion.models import PromotionPackage

from .models import Product, Category
from .errors import *


class ProductBL(BaseLogic):

    def _is_code_duplicate(self, code, id=None):
        params = dict(
            code=code
        )
        if id:
            params['id__ne'] = id

        return Product.objects(**params).first()

    def get(self, id=None, slug=None):
        if not id and not slug:
            raise InvalidRequestParams('Must pass atleast code or slug!')

        params = dict(
            deleted=False
        )

        if id:
            params['id'] = id

        else:
            params['slug'] = slug

        product = Product.objects(**params).first()

        if not product:
            raise InvalidRequestParams('Product not found!')

        result = product.output()
        for index, image_id in enumerate(product.images):
            image = Image.objects(id=image_id).first()
            result['images'][index] = image.url

        if product.promotion_package_id:
            promotion_package = PromotionPackage.objects(id=product.promotion_package_id).first()
            result['sale_off_value'] = promotion_package.sale_off_value

        return result

    def create(self, category_id, name, price=None, code=None,
               status=None, sizes=None, promotion_package_id=None):

        product = Product()
        product.name = name
        product.category_id = category_id

        category = self._get_record_by_id(model=Category, id=category_id)
        product.category_id = category.id

        if price:
            product.price = price

        if not status:
            product.status = 'available'

        if sizes:
            product.sizes = sizes

        if promotion_package_id:
            self._get_record_by_id(model=PromotionPackage, id=promotion_package_id)
            product.promotion_package_id = promotion_package_id

        if code:
            if self._is_code_duplicate(code=code):
                raise DuplicateCode
            product.code = code

        product.create()
        return product.output()

    def update(self, id, name=None, price=None, default_image_id=None, code=None,
               status=None, sizes=None, promotion_package_id=None):

        product = self._get_record_by_id(model=Product, id=id)

        update_params = dict()

        if name:
            update_params['name'] = name

        if price is not None:
            update_params['price'] = price

        if sizes is not None:
            update_params['sizes'] = sizes

        if status:
            update_params['status'] = status

        if code:
            if self._is_code_duplicate(code=code, id=id):
                raise DuplicateCode
            update_params['code'] = code

        if promotion_package_id:
            self._get_record_by_id(model=PromotionPackage, id=promotion_package_id)
        update_params['promotion_package_id'] = promotion_package_id

        if default_image_id:
            if default_image_id not in product.images:
                raise InvalidRequestParams('Default image id not in product images!')
            update_params['default_image_id'] = default_image_id

        if update_params:
            product.patch(update_params=update_params)

        return dict(success=True)

    def list(self, page, per_page, order, categories=None, search_text=None, statuses=None, is_sale_off=None):
        params = dict()
        if categories:
            params['category_id__in'] = categories

        if statuses:
            params['status__in'] = statuses

        matches = Product.objects(**params)

        if is_sale_off:
            matches = matches.filter(__raw__={'promotion_package_id': {'$ne': None}})

        if search_text:
            search_text_query = Q(slug__contains=slugify(search_text)) | \
                                Q(code__contains=search_text)
            matches = matches.filter(search_text_query)
        matches = matches.order_by(order)
        total = matches.count(True)

        result = []

        for product in matches.paginate(page=page, per_page=per_page).items:
            product_output = product.output()
            for index, image_id in enumerate(product.images):
                image = Image.objects(id=image_id).first()
                product_output['images'][index] = image.url

            if product.promotion_package_id:
                promotion_package = PromotionPackage.objects(id=product.promotion_package_id).first()
                product_output['sale_off_value'] = promotion_package.sale_off_value
            result.append(product_output)

        return dict(total=total, result=result)


class CategoryBL(BaseLogic):

    def create(self, name, parent_id=None):

        if self.is_name_duplicate(name):
            deleted_category = Category.objects(slug=slugify(name), deleted=True).first()
            if not deleted_category:
                raise NameAlreadyExists

            category = deleted_category

        else:
            category = Category()
            category.name = name

        if parent_id:
            category.parent_id = parent_id

        category.create()
        return category.output()

    def update(self, id, name=None, parent_id=None):

        category = self._get_record_by_id(model=Category, id=id)

        update_params = dict()

        if name:
            if self.is_name_duplicate(name=name, id=id):
                raise NameAlreadyExists
            update_params['name'] = name

        if parent_id:
            parent = Category.objects(parent_id__exists=False, id=parent_id).first()
            if not parent:
                raise InvalidRequestParams('Parent not found!')
            update_params['parent_id'] = parent_id

        if update_params:
            category.patch(update_params=update_params)

        return dict(success=True)

    def delete(self, id):
        category = self._get_record_by_id(model=Category, id=id)
        category.patch(update_params=dict(deleted=True))
        return dict(success=True)

    def list(self, page, per_page, order, get_parents=None, parent_id=None, name=None):
        params = dict(deleted=False)

        if name:
            params['slug__contains'] = slugify(name)

        if get_parents:
            params['parent_id__exists'] = False

        elif parent_id:
            parent_id['parent_id'] = parent_id

        matches = Category.objects(**params).order_by(order)
        total = matches.count(True)

        result = []

        for category in matches.paginate(page=page, per_page=per_page).items:
            category_output = category.output()
            result.append(category_output)

        return dict(total=total, result=result)

    def get_one(self, id):
        category = self._get_record_by_id(model=Category, id=id)
        result = category.output()
        for index, image_id in enumerate(category.images):
            image = Image.objects(id=image_id).first()
            result['images'][index] = image.url
        return result

    def is_name_duplicate(self, name, id=None):
        params = dict(slug=slugify(name))
        if id:
            params['id__ne'] = id
        return Category.objects(**params).first() is not None


product_bl = ProductBL()
category_bl = CategoryBL()
