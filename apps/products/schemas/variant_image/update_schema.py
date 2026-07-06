from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

from apps.products.serializers.request.variant_image_request_serializers.variant_image_request import (
    VariantImageRequestSerializer,
)
from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageDetailResponseSerializer,
)


variant_image_update_schema = extend_schema(

    tags=["Variant Images"],

    summary="Update Variant Image",

    description="""
Update an existing variant image.
""",

    request=VariantImageRequestSerializer,

    responses={
        200: VariantImageDetailResponseSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Variant image not found."
                }
            },
        },
    },

    examples=[
        OpenApiExample(
            name="Update Variant Image",

            request_only=True,

            value={
                "variant": 1,
                "image": "<FILE>",
                "alt_text": "Updated Front View",
                "is_main": True,
                "position": 1,
            },
        ),
    ],
)