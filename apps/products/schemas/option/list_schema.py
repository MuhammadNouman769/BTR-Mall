from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.variant_response import (
    ProductVariantResponseSerializer
)


variant_list_schema = extend_schema(
    summary="List Product Variants",

    responses=ProductVariantResponseSerializer(many=True),

    tags=["Variants"]
)