from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.shop_restore_request_list import (
    ShopRestoreRequestSerializer
)

shop_restore_request_list_schema = extend_schema(
    summary="List Shop Restore Requests (Admin)",
    description="Admin can view all restore requests (pending/approved/rejected).",
    responses=ShopRestoreRequestSerializer(many=True),
)

shop_restore_request_detail_schema = extend_schema(
    summary="Shop Restore Request Detail (Admin)",
    description="Get full detail of a single restore request.",
    responses=ShopRestoreRequestSerializer,
)