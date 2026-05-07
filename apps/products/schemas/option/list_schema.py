from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.option_response import ProductOptionResponseSerializer


option_list_schema = extend_schema(
    responses=ProductOptionResponseSerializer(many=True)
)