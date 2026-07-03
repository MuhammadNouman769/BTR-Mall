from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionListResponseSerializer,
)


option_list_schema = extend_schema(
    operation_id="option_list",
    responses=ProductOptionListResponseSerializer
)