from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductReview

from apps.products.serializers.response.admin_approvel_response_serializers.review_response import (
    ProductReviewResponseSerializer
)

from apps.products.schemas.review.detail_schema import (
    review_detail_schema
)

@extend_schema_view(
    get=review_detail_schema
)
class ProductReviewDetailAPIView(RetrieveAPIView):

    permission_classes = [AllowAny]

    serializer_class = ProductReviewResponseSerializer

    lookup_field = "id"

    queryset = ProductReview.objects.select_related(
        "user",
        "product"
    ).prefetch_related(
        "images"
    ).filter(
        is_deleted=False,
        is_approved=True
    )