from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantDetailResponseSerializer,
)

variant_detail_schema = extend_schema(
    operation_id="variant_detail",
    tags=["Variants"],
    summary="Variant Detail",
    description="Retrieve details of a single product variant.",
    responses={
        200: ProductVariantDetailResponseSerializer,
    },
)