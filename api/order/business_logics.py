from slugify import slugify
from mongoengine import Q
from flask import request, g

from api.common.base_logics import BaseLogic
from api.common.base_errors import InvalidRequestParams, PermissionError
from api.storage.models import Image
from api.product.models import Product
from api.promotion.models import PromotionPackage

from .models import Order, OrderItem, OrderCreator
from .errors import *


class OrderBL(BaseLogic):

    def get(self, id):
        product = self._get_record_by_id(model=Order, id=id)
        result = product.output()
        return result

    def create(self, order_items, order_creator, description=None):

        order = Order()
        order.status = 'in-progress'
        if description:
            order.description = description

        creator_info = OrderCreator()
        creator_info.ip = request.remote_addr

        creator_name = order_creator.get('name')
        if creator_name:
            creator_info.name = creator_name
            creator_info.slug = slugify(creator_name)

        creator_address = order_creator.get('address')
        if creator_address:
            creator_info.address = creator_address

        creator_info.email = order_creator['email']
        creator_info.phone = order_creator['phone']

        creator_info.check_required_fields()

        order.creator_info = creator_info

        items = []
        total = 0
        for item_data in order_items:
            product_id = item_data['product_id']
            count = item_data['count']
            metadata = item_data.get('metadata')

            product = self._get_record_by_id(model=Product, id=product_id)

            item = OrderItem()

            if len(product.images):
                image = Image.objects(id=product.images[0]).first()
                item.product_image_url = image.url

            item.product_id = product.id
            item.product_category = product.category_id
            item.product_name = product.name
            item.product_slug = product.slug
            item.product_price = product.price
            item.count = count

            discount = 0
            promotion_package_id = product.promotion_package_id
            if promotion_package_id:
                promotion_package = PromotionPackage.objects(id=promotion_package_id).first()
                discount = promotion_package.sale_off_value / 100

            item.total = product.price * (1 - discount) * count

            if metadata:
                item.metadata = metadata

            item.check_required_fields()

            total += item.total

            items.append(item)

        order.total = total
        order.items = items
        order.create()
        return order.output()

    def update(self, id, status=None):

        order = self._get_record_by_id(model=Order, id=id)
        if order.status in ['success', 'canceled']:
            raise InvalidRequestParams('Order is already done! Cannot be edited!')

        update_params = dict()

        if status:
            update_params['status'] = status

        if update_params:
            update_params['updated_by'] = g.user.id
            order.patch(update_params=update_params)

        return dict(success=True)

    def list(self, page, per_page, order, search_text=None, total_min=None, total_max=None):
        params = dict()
        if total_min:
            params['total__gte'] = total_min

        if total_max:
            params['total__lte'] = total_max

        matches = Order.objects(**params)

        if search_text:
            search_text_query = Q(items__product_slug__contains=slugify(search_text)) | \
                                Q(creator_info__email__contains=search_text) | \
                                Q(creator_info__slug__contains=slugify(search_text)) | \
                                Q(creator_info__address__contains=search_text) | \
                                Q(creator_info__phone__contains=search_text)
            matches = matches.filter(search_text_query)
        matches = matches.order_by(order)
        total = matches.count(True)

        result = []

        for product in matches.paginate(page=page, per_page=per_page).items:
            product_output = product.output()
            result.append(product_output)

        return dict(total=total, result=result)


order_bl = OrderBL()
