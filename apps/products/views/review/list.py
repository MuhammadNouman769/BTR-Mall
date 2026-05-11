from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from apps.products.serializers.response.review_response import (
    ProductReviewResponseSerializer
)

from apps.products.selectors.review_selector import (
    ProductReviewSelector
)
from apps.products.schemas.review.list_schema import (
review_list_schema
)
from drf_spectacular.utils import extend_schema_view


from drf_yasg.utils import swagger_auto_schema

@extend_schema_view(
    get=review_list_schema
)
class ProductReviewListAPIView(ListAPIView):

    serializer_class = ProductReviewResponseSerializer

    def get_queryset(self):

        return ProductReviewSelector.get_product_reviews(
            self.kwargs["product_id"]
        )