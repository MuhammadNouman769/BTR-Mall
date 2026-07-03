from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

from apps.products.serializers.request.variant_request_serializers.variant_request import (
    ProductVariantCreateSerializer,
)


variant_update_schema = extend_schema(
    tags=["Variants"],

    summary="Update Variant",

    description="""
Update an existing product variant.

Variant images are managed separately using the Variant Images API.
""",

    request=ProductVariantCreateSerializer,

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Variant updated successfully."
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
            name="Update Variant",
            request_only=True,
            value={
                "product": 1,
                "sku": "SKU-001",
                "barcode": "123456789",

                "option1": 1,
                "option2": 2,

                "price": "1400.00",
                "compare_at_price": "1600.00",

                "stock_quantity": 25,

                "track_inventory": True,
                "allow_backorder": False,

                "position": 1,
            },
        ),
    ],
)