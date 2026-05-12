from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.product_response import ProductDetailSerializer


product_detail_schema = extend_schema(
    tags=["Products"],
    summary="Product Detail",
    responses=ProductDetailSerializer,
    description="Get full product detail including variants, options, images"
)