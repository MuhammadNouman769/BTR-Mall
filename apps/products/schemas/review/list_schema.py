from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from apps.products.serializers.response.admin_approvel_response_serializers.review_response import (
    ProductReviewResponseSerializer
)


review_list_schema = extend_schema(

    tags=["Product Reviews"],

    summary="List Product Reviews",

    description="""
    Get all approved reviews of a product.
    """,

    parameters=[
        OpenApiParameter(
            name="product",
            required=True,
            type=int,
            location=OpenApiParameter.QUERY,
            description="Product ID"
        )
    ],

    responses={
        200: ProductReviewResponseSerializer(many=True)
    }
)