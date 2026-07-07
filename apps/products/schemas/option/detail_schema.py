from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionDetailResponseSerializer,
)


option_detail_schema = extend_schema(

    operation_id="option_detail",

    tags=["Options"],

    summary="Option Detail",

    description="""
Retrieve details of a single product option along with all of its values.
""",

    responses={
        200: ProductOptionDetailResponseSerializer,
    },
)