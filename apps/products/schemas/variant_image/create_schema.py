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


variant_image_create_schema = extend_schema(
    operation_id="variant_image_create",

    tags=["Variant Images"],

    summary="Create Variant Image",

    description="""
Upload a single image for a product variant.

To upload multiple images, call this endpoint multiple times.
""",

    request=VariantImageRequestSerializer,

    responses={
        201: VariantImageDetailResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Create Variant Image",

            request_only=True,

            value={
                "variant": 1,
                "image": "<FILE>",
                "alt_text": "Front View",
                "is_main": True,
                "position": 1,
            },
        ),
    ],
)