from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.products.serializers.request.variant_request import (
    ProductVariantCreateSerializer
)

from apps.products.serializers.response.variant_response import (
    ProductVariantResponseSerializer
)


variant_create_schema = extend_schema(
    summary="Create Product Variant",

    request=ProductVariantCreateSerializer,

    responses=ProductVariantResponseSerializer,

    examples=[
        OpenApiExample(
            "Variant Create Example",
            value={
                "product": 1,
                "sku": "IPHONE-15-BLACK-128",
                "barcode": "123456789",

                "option1": 1,
                "option2": 2,

                "price": "450000",
                "compare_at_price": "500000",

                "stock_quantity": 10,

                "track_inventory": True,
                "allow_backorder": False,

                "position": 1
            }
        )
    ],

    tags=["Variants"]
)