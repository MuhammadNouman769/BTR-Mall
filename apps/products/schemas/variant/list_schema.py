from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantListResponseSerializer,
)


variant_list_schema = extend_schema(
    operation_id="variant_list",

    tags=["Variants"],

    summary="List Variants",

    description="""
Retrieve a list of all product variants.

Each variant includes:
- Variant information
- Stock details
- Pricing
- Variant images
""",

    responses={
        200: ProductVariantListResponseSerializer,
    },
)