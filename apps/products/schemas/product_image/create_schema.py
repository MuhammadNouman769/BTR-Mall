from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiRequest,
)

from apps.products.serializers.request.product_image_request_serializers.product_image_request import (
    ProductImageCreateSerializer,
)

from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
    ProductImageResponseSerializer,
)


product_image_create_schema = extend_schema(

    tags=["Product Images"],

    summary="Create Product Image",

    description="""
Upload a single image for a product.
""",

    request=OpenApiRequest(
        request=ProductImageCreateSerializer,
        encoding={
            "image": {
                "contentType": "image/*",
            },
        },
    ),

    responses={
        201: ProductImageResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Create Product Image",
            request_only=True,
            value={
                "product": 1,
                "image": "<FILE>",
                "alt_text": "Front View",
                "position": 1,
            },
        ),
    ],
)