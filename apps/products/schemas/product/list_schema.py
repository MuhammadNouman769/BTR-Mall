from drf_spectacular.utils import extend_schema
from apps.products.serializers.response.product_response import ProductListSerializer


product_list_schema = extend_schema(
    tags=["Products"],
    summary="Product List",
    description="""
    Returns a paginated list of products.

    Each product includes:
    - Basic product info (title, description)
    - Main image
    - Starting price from variants
    - Shop information (if needed)
    - Categories (if included in serializer)
    """,
    responses={
        200: ProductListSerializer(many=True)
    }
)