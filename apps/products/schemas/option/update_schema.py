from drf_spectacular.utils import extend_schema

from apps.products.serializers.request.variant_request import (
    ProductVariantCreateSerializer
)

from apps.products.serializers.response.variant_response import (
    ProductVariantResponseSerializer
)


variant_update_schema = extend_schema(
    summary="Update Variant",

    request=ProductVariantCreateSerializer,

    responses=ProductVariantResponseSerializer,

    tags=["Variants"]
)