from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
    ProductImageListResponseSerializer,
)


product_image_list_schema = extend_schema(
    operation_id="product_image_list",
    tags=["Product Images"],
    summary="List Product Images",
    description="""
Retrieve all product images.

Optionally filter by product ID.
""",
    parameters=[
        OpenApiParameter(
            name="product",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter images by product ID.",
        ),
    ],
    responses={
        200: ProductImageListResponseSerializer,
    },
)