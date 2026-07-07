from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionListResponseSerializer,
)


option_list_schema = extend_schema(

    operation_id="option_list",

    tags=["Options"],

    summary="List Options",

    description="""
Retrieve a list of all product options with their values.
""",

    responses={
        200: ProductOptionListResponseSerializer,
    },
)