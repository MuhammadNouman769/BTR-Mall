from drf_spectacular.utils import extend_schema

from apps.products.serializers.request.admin_approvel_request_serializers.shop_restore_request import (
    SellerShopRestoreRequestSerializer
)

from apps.products.serializers.response.admin_approvel_response_serializers.shop_restore_response import (
    SellerShopRestoreResponseSerializer
)


shop_restore_request_schema = extend_schema(
    tags=["Shop Restore"],

    summary="Request Shop Restore",

    description="""
    Seller can request restoration of a deleted shop.
    Request goes to admin for approval.
    """,

    request=SellerShopRestoreRequestSerializer,

    responses={
        200: SellerShopRestoreResponseSerializer,
        400: {"example": {"error": "Restore request already submitted"}},
        404: {"example": {"error": "Shop not found"}},
    }
)