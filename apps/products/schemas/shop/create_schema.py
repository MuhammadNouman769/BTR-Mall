from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse
)

from apps.products.serializers.request.shop_create_request_serializers.shop_create import (
    ShopCreateSerializer
)


shop_create_schema = extend_schema(
    tags=["Shop"],

    operation_id="create_shop",

    summary="Create Shop",

    description="""
Create a new seller shop.

Requirements:
- User must be authenticated
- User role must be seller
- One seller can only create one shop
""",

    request=ShopCreateSerializer,

    responses={
        201: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Shop created successfully"
                    },
                    "id": {
                        "type": "integer",
                        "example": 1
                    }
                }
            },
            description="Shop created successfully"
        ),

        400: OpenApiResponse(
            description="Validation error"
        ),

        403: OpenApiResponse(
            description="Permission denied"
        )
    },

    examples=[
        OpenApiExample(
            name="Create Shop Example",

            summary="Basic shop creation payload",

            description="Example request body for creating a seller shop",

            value={
                "name": "BTR Store",

                "description": "Best electronics store in Pakistan",

                "cnic_number": "1234567890123"
            },

            request_only=True,
        )
    ]
)