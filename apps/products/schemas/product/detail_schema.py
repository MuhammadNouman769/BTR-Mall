from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.product_response_serializers.product_response import ProductDetailResponseSerializer


product_detail_schema = extend_schema(
    tags=["Products"],
    summary="Product Detail",

    description="""
    Returns full product detail including:

    - Product basic info
    - Categories
    - Images
    - Options
    - Variants with stock & pricing
    - Shop info
    """,

    responses=ProductDetailResponseSerializer
)