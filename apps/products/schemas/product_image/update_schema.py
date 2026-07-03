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


product_image_update_schema = extend_schema(

    tags=["Product Images"],

    summary="Update Product Image",

    description="""
Update an existing product image.
Supports both PUT and PATCH requests.
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
        200: ProductImageResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Update Product Image",
            request_only=True,
            value={
                "product": 1,
                "image": "<FILE>",
                "alt_text": "Updated Front View",
                "position": 2,
            },
        ),
    ],
)