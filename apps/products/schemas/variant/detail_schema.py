from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantDetailResponseSerializer,
)


variant_detail_schema = extend_schema(
    operation_id="variant_detail",

    tags=["Variants"],

    summary="Variant Detail",

    description="""
Retrieve complete details of a single product variant.

Variant images are included in the response.
""",

    parameters=[
        OpenApiParameter(
            name="pk",
            type=int,
            location=OpenApiParameter.PATH,
            description="Variant ID",
            required=True,
        ),
    ],

    responses={
        200: ProductVariantDetailResponseSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Variant not found."
                }
            },
        },
    },
)