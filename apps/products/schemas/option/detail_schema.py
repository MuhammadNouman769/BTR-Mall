from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.option_response_serializers.option_response import ProductOptionResponseSerializer


option_detail_schema = extend_schema(
    operation_id="option_detail",
    responses=ProductOptionResponseSerializer,
    summary="Option Detail",
    description="Get single product option with values"
)