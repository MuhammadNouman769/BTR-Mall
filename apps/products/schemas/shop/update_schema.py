from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse
)

from apps.products.serializers.request.shop_create_request_serializers.shop_update import (
    ShopUpdateSerializer
)

from apps.products.serializers.response.shop_create_response_serializers.shop_response import (
    ShopDetailSerializer
)


shop_update_schema = extend_schema(
    tags=["Shop"],

    operation_id="update_shop",

    summary="Update Shop",

    description="""
Update authenticated seller shop information.

Supports partial updates including:
- name
- description
- logo
- banner
- CNIC information
""",

    request=ShopUpdateSerializer,

    responses={
        200: OpenApiResponse(
            response=ShopDetailSerializer,
            description="Shop updated successfully"
        ),

        400: OpenApiResponse(
            description="Validation error"
        ),

        401: OpenApiResponse(
            description="Authentication required"
        ),

        404: OpenApiResponse(
            description="Shop not found"
        )
    }
)