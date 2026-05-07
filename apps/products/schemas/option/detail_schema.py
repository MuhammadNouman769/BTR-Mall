from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.variant_response import (
    ProductVariantResponseSerializer
)


variant_detail_schema = extend_schema(
    summary="Variant Detail",

    responses=ProductVariantResponseSerializer,

    tags=["Variants"]
)