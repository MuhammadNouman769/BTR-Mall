from drf_spectacular.utils import extend_schema

from apps.products.serializers.response.review_response import (
    ProductReviewResponseSerializer
)


review_detail_schema = extend_schema(

    tags=["Product Reviews"],

    summary="Review Detail",

    description="Get single review detail",

    responses={
        200: ProductReviewResponseSerializer
    }
)