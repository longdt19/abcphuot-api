from slugify import slugify
from mongoengine import Q

from api.common.base_logics import BaseLogic
from api.common.base_errors import InvalidRequestParams, PermissionError
from api.storage.models import Image
from api.promotion.models import PromotionPackage

from .models import Product, Category, SimProduct, WifiProduct
from .errors import *

class WifiProductBL(BaseLogic):

    def list(self, page, per_page, order, search_text=None):
        matches = WifiProduct.objects()
        print ('matches', matches)

        if search_text:
            search_text_query = Q(slug__contains=slugify(search_text)) | \
                                Q(code__contains=search_text)
            matches = matches.filter(search_text_query)
        matches = matches.order_by(order)
        total = matches.count(True)

        result = []

        for product in matches.paginate(page=page, per_page=per_page).items:
            product_output = product.output()
            image_id = product.image
            # for index, image_id in enumerate(product.image):
            if image_id:
                image = Image.objects(id=image_id).first()
                print ('image', image.url)
                print ('path', image.path)
            product_output['image'] = image.url
            result.append(product_output)

        return dict(total=total, result=result)

    def create(self, country, internet_name, connection, speed_download,
               speed_upload, information, prepayment, price_day, image_id, continent):
        product = WifiProduct(country=country,
                              internet_name=internet_name,
                              connection=connection,
                              speed_download=speed_download,
                              speed_upload=speed_upload,
                              information=information,
                              prepayment=prepayment,
                              price_day=price_day,
                              image=image_id,
                              continent=continent)
        product.create()
        product.save()
        return product.output()
    
    def update(self, id, country, internet_name, connection, speed_download,
               speed_upload, information, prepayment, price_day, continent):
        product = self._get_record_by_id(model=WifiProduct, id=id)
        update_params = dict()
        if country:
            update_params['country'] = country
        if internet_name:
            update_params['internet_name'] = internet_name
        if connection:
            update_params['connection'] = connection
        if speed_download:
            update_params['speed_download'] = speed_download
        if speed_upload:
            update_params['speed_upload'] = speed_upload
        if information:
            update_params['information'] = information
        if prepayment:
            update_params['prepayment'] = prepayment
        if price_day:
            update_params['price_day'] = price_day
        if continent:
            update_params['continent'] = continent

        if update_params:
            product.patch(update_params=update_params)

        return (product.output())
    
    def delete(self, id):
        product = self._get_record_by_id(model=WifiProduct, id=id)
        product.delete()
        product.save()
        return dict(success=True)

class SimProductBL(BaseLogic):

    def list(self, page, per_page, order, search_text=None):
        matches = SimProduct.objects()

        if search_text:
            search_text_query = Q(slug__contains=slugify(search_text)) | \
                                Q(code__contains=search_text)
            matches = matches.filter(search_text_query)
        matches = matches.order_by(order)
        total = matches.count(True)

        result = []

        for product in matches.paginate(page=page, per_page=per_page).items:
            product_output = product.output()
            image_id = product.image
            # for index, image_id in enumerate(product.image):
            if image_id:
                image = Image.objects(id=image_id).first()
                print ('image', image.url)
                print ('path', image.path)
            product_output['image'] = image.url
            result.append(product_output)

        return dict(total=total, result=result)
    
    def create(self, owned, day_used, price, image_id, country):
        product = SimProduct(owned=owned,
                             day_used=day_used,
                             price=price,
                             image=image_id,
                             country=country)
        product.create()
        product.save()
        return product.output()
    
    def update(self, id, owned, day_used, price, country):
        product = self._get_record_by_id(model=SimProduct, id=id)

        update_params = dict()
        if owned:
            update_params['owned'] = owned
        if day_used:
            update_params['day_used'] = day_used
        if price:
            update_params['price'] = price
        if country:
            update_params['country'] = country

        if update_params:
            product.patch(update_params=update_params)
        
        return (product.output())
    
    def delete(self, id):
        product = self._get_record_by_id(model=SimProduct, id=id)
        product.delete()
        product.save()
        return dict(success=True)

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
sim_bl = SimProductBL()
wifi_bl = WifiProductBL()
