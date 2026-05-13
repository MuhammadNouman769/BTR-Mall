from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from apps.products.serializers.request.review_serializers.update_review import (
    ProductReviewUpdateSerializer
)

from apps.products.serializers.response.admin_approvel_response_serializers.review_response import (
    ProductReviewResponseSerializer
)


review_update_schema = extend_schema(

    tags=["Product Reviews"],

    summary="Update Review",

    description="""
    User can update own review.
    """,

    request=ProductReviewUpdateSerializer,

    responses={

        200: ProductReviewResponseSerializer,

        400: OpenApiResponse(
            description="Validation Error"
        ),

        404: OpenApiResponse(
            description="Review Not Found"
        ),
    }
)