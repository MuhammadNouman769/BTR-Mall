from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

from apps.products.serializers.request.variant_request_serializers.variant_request import (
    ProductVariantCreateSerializer,
)


variant_create_schema = extend_schema(
    tags=["Variants"],

    summary="Create Variant",

    description="""
Create a new product variant.

Variant images are uploaded separately using the Variant Images API.
""",

    request=ProductVariantCreateSerializer,

    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Variant created successfully."
                },
                "id": {
                    "type": "integer",
                    "example": 1
                },
            },
        },
    },

    examples=[
        OpenApiExample(
            name="Create Variant",

            value={
                "product": 1,
                "sku": "SKU-001",
                "barcode": "123456789",

                "option1": 1,
                "option2": 2,

                "price": "1200.00",
                "compare_at_price": "1500.00",

                "stock_quantity": 10,

                "track_inventory": True,
                "allow_backorder": False,

                "position": 1,
            },

            request_only=True,
        ),
    ],
)