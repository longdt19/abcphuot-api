from api.common.base_logics import BaseLogic
from api.product.models import Category as ProductCategory
from api.product.constants import PRODUCT_STATUSES, PRODUCT_SIZES
from api.post.constants import POST_CATEGORIES
from api.order.constants import ORDER_STATUSES


class EntranceBL(BaseLogic):
    def get_constants(self):
        return dict(
            product_categories=[record.output() for record in ProductCategory.objects(deleted=False)],
            product_statuses=PRODUCT_STATUSES,
            product_sizes=PRODUCT_SIZES,
            post_categories=POST_CATEGORIES,
            order_statuses=ORDER_STATUSES
        )


entrance_bl = EntranceBL()
