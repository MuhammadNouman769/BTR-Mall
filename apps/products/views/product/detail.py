from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.product_selector import ProductSelector
from apps.products.serializers.response.product_response import (
    ProductDetailSerializer
)
from apps.products.schemas.product.detail_schema import (
    product_detail_schema
)


@extend_schema_view(
    get=product_detail_schema
)
class ProductDetailAPIView(RetrieveAPIView):

    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_object(self):

        try:
            return ProductSelector.detail(
                pk=self.kwargs["id"]
            )

        except Exception:
            raise NotFound({
                "error": "Product not found"
            })