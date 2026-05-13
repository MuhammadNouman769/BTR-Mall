from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse
)

from apps.products.serializers.response.shop_create_response_serializers.shop_response import (
    ShopDetailSerializer
)


shop_detail_schema = extend_schema(
    tags=["Shop"],

    operation_id="shop_detail",

    summary="Shop Detail",

    description="""
Retrieve complete shop details by ID.
""",

    responses={
        200: OpenApiResponse(
            response=ShopDetailSerializer,
            description="Shop detail retrieved successfully"
        ),

        404: OpenApiResponse(
            description="Shop not found"
        )
    }
)