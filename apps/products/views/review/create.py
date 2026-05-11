from drf_spectacular.utils import extend_schema_view
from jsonschema.validators import extend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.products.models.product import Product

from apps.products.serializers.request.review_serializers.review_create import (
    ProductReviewCreateSerializer
)

from apps.products.serializers.response.review_response import (
    ProductReviewResponseSerializer
)

from apps.products.services.review_service import (
    ProductReviewService
)
from rest_framework.parsers import MultiPartParser, FormParser


from apps.products.schemas.review.create_schema import review_create_schema

@extend_schema_view(
    post=review_create_schema,
)
class ProductReviewCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    serializer_class = ProductReviewCreateSerializer

    def post(self, request, product_id):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        review = ProductReviewService.create_review(
            user=request.user,
            product=product,
            validated_data=serializer.validated_data
        )

        return Response(
            {
                "message": "Review submitted successfully",
                "data": ProductReviewResponseSerializer(review).data
            },
            status=status.HTTP_201_CREATED
        )