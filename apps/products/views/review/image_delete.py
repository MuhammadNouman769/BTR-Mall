from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductReviewImage

from apps.products.schemas.review.image_delete_schema import (
    review_image_delete_schema
)


@extend_schema_view(
    delete=review_image_delete_schema
)
class ProductReviewImageDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        try:
            image = ProductReviewImage.objects.select_related(
                "review"
            ).get(
                id=id,
                review__user=request.user,
                is_deleted=False
            )

        except ProductReviewImage.DoesNotExist:
            return Response(
                {
                    "error": "Review image not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        image.delete()

        return Response(
            {
                "message": "Review image deleted successfully"
            },
            status=status.HTTP_200_OK
        )