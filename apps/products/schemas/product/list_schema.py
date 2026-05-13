from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.product_response_serializers.product_response import ProductListResponseSerializer

product_list_schema = extend_schema(
    tags=["Products"],
    summary="Product List",
    description="Returns products with filters",
    responses=ProductListResponseSerializer(many=True)
)