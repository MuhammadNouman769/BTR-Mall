from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.variant_request_serializers.variant_request import ProductVariantCreateSerializer


variant_create_schema = extend_schema(
    request=ProductVariantCreateSerializer,
    responses={201: {"message": "Variant created successfully"}},

    examples=[
        OpenApiExample(
            "Create Variant",
            value={
                "product": 1,
                "sku": "SKU-001",
                "price": 1200,
                "stock_quantity": 10,
                "images": [
                    {
                        "alt_text": "front view",
                        "is_main": True
                    }
                ]
            }
        )
    ]
)