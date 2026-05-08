from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.shop_restore_response import (
    ShopRestoreResponseSerializer
)


shop_restore_approve_schema = extend_schema(
    tags=["Shop Restore Admin"],

    summary="Approve Shop Restore Request",

    description="""
    Admin approves deleted shop restore request.
    Shop becomes active again.
    """,

    responses={
        200: ShopRestoreResponseSerializer,
        400: {"example": {"error": "This request has already been processed"}},
        404: {"example": {"error": "Restore request not found"}},
    }
)