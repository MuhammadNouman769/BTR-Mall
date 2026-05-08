from drf_spectacular.utils import extend_schema

from apps.products.serializers.request.shop_restore_request import (
    ShopRestoreRequestSerializer
)

from apps.products.serializers.response.shop_restore_response import (
    ShopRestoreResponseSerializer
)


shop_restore_request_schema = extend_schema(
    tags=["Shop Restore"],

    summary="Request Shop Restore",

    description="""
    Seller can request restoration of a deleted shop.
    Request goes to admin for approval.
    """,

    request=ShopRestoreRequestSerializer,

    responses={
        200: ShopRestoreResponseSerializer,
        400: {"example": {"error": "Restore request already submitted"}},
        404: {"example": {"error": "Shop not found"}},
    }
)