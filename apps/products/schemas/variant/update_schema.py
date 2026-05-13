from drf_spectacular.utils import extend_schema
from apps.products.serializers.request.variant_request_serializers.variant_request import ProductVariantCreateSerializer


variant_update_schema = extend_schema(
    request=ProductVariantCreateSerializer,
    responses={200: {"message": "Variant updated successfully"}}
)