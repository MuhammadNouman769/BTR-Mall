from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
    ProductImageResponseSerializer,
)


product_image_detail_schema = extend_schema(
    operation_id="product_image_detail",


    tags=["Product Images"],

    summary="Product Image Detail",

    description="""
Retrieve a single product image by its ID.
""",

    responses={
        200: ProductImageResponseSerializer,
    },
)