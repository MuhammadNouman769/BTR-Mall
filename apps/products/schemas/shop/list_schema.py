from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse
)

from apps.products.serializers.response.shop_create_response_serializers.shop_response import (
    ShopListSerializer
)


shop_list_schema = extend_schema(
    tags=["Shop"],

    operation_id="shop_list",

    summary="Shop List",

    description="""
Retrieve a list of all shops.

Supports:
- Admin listing
- Public shop listing
""",

    responses={
        200: OpenApiResponse(
            response=ShopListSerializer(many=True),
            description="Shops retrieved successfully"
        )
    }
)