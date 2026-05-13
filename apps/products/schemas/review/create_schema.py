from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from apps.products.serializers.request.review_serializers.review_create import (
    ProductReviewCreateSerializer
)

from apps.products.serializers.response.admin_approvel_response_serializers.review_response import (
    ProductReviewResponseSerializer
)


review_create_schema = extend_schema(

    tags=["Product Reviews"],

    summary="Create Product Review",

    description="""
    Customer can create a review for a product.

    Features:
    - Rating
    - Comment
    - Multiple image upload
    - One review per user per product
    """,

    request=ProductReviewCreateSerializer,

    responses={

        201: ProductReviewResponseSerializer,

        400: OpenApiResponse(
            description="Validation Error"
        ),

        401: OpenApiResponse(
            description="Authentication Required"
        ),
    }
)