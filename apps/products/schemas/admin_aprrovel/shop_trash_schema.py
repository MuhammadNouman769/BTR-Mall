from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.shop_trash_response import ShopTrashSerializer


shop_trash_schema = extend_schema(
    summary="Get all soft deleted shops (Trash)",
    responses=ShopTrashSerializer(many=True)
)