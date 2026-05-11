from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models.review import ProductReview
from apps.products.schemas.review.delete_schema import review_delete_schema

@extend_schema_view(delete=review_delete_schema)
class ProductReviewDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated]

    queryset = ProductReview.objects.all()

    lookup_field = "id"

    def get_queryset(self):

        return ProductReview.objects.filter(
            user=self.request.user
        )