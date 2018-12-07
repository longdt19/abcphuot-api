from api.entrance.resources import RESOURCES as ENTRANCE_RESOURCES
from api.product.resources import RESOURCES as PRODUCT_RESOURCES
from api.storage.resources import RESOURCES as STORAGE_RESOURCES
from api.user.resources import RESOURCES as USER_RESOURCES
from api.post.resources import RESOURCES as POST_RESOURCES
from api.order.resources import RESOURCES as ORDER_RESOURCES
from api.promotion.resources import RESOURCES as PROMOTION_RESOURCES

ENDPOINTS = {
    **ENTRANCE_RESOURCES,
    **PRODUCT_RESOURCES,
    **STORAGE_RESOURCES,
    **USER_RESOURCES,
    **POST_RESOURCES,
    **ORDER_RESOURCES,
    **PROMOTION_RESOURCES,
}
