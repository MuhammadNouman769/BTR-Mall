from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer,
)

product_detail_schema = extend_schema(

    tags=["Products"],

    summary="Product Detail",

    description="Retrieve a product by its ID.",

    responses={
        200: ProductDetailResponseSerializer,
    },
)