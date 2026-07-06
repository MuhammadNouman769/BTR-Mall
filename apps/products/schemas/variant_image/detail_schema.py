from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageDetailResponseSerializer,
)


variant_image_detail_schema = extend_schema(
    operation_id="variant_image_detail",

    tags=["Variant Images"],

    summary="Variant Image Detail",

    description="""
Retrieve details of a single variant image.
""",

    parameters=[
        OpenApiParameter(
            name="pk",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="Variant Image ID",
        ),
    ],

    responses={
        200: VariantImageDetailResponseSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Variant image not found.",
                }
            },
        },
    },
)