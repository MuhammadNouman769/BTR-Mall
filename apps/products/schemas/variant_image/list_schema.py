from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageListResponseSerializer,
)


variant_image_list_schema = extend_schema(
    operation_id="variant_image_list",

    tags=["Variant Images"],

    summary="List Variant Images",

    description="""
Retrieve a list of all variant images.
""",

    responses={
        200: VariantImageListResponseSerializer,
    },
)