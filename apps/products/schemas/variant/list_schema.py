from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.variant_response import ProductVariantResponseInProductSerializer


variant_list_schema = extend_schema(
    responses=ProductVariantResponseInProductSerializer(many=True),
    description="List all product variants"
)