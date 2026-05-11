from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductReview

from apps.products.serializers.request.review_serializers.update_review import (
    ProductReviewUpdateSerializer
)

from apps.products.serializers.response.review_response import (
    ProductReviewResponseSerializer
)

from apps.products.schemas.review.update_schema import (
    review_update_schema
)

from apps.products.services.review_service import (
    ProductReviewService
)


@extend_schema_view(
    patch=review_update_schema
)
class ProductReviewUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    serializer_class = ProductReviewUpdateSerializer

    def patch(self, request, id):

        review = ProductReview.objects.get(
            id=id,
            user=request.user
        )

        serializer = ProductReviewUpdateSerializer(
            review,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        review = ProductReviewService.update_review(
            review,
            serializer.validated_data
        )

        return Response({
            "message": "Review updated successfully",
            "data": ProductReviewResponseSerializer(
                review,
                context={"request": request}
            ).data
        })