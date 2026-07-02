from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.product_selector import ProductSelector
from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductListResponseSerializer
)
from apps.products.pagination import ProductPagination
from apps.products.schemas.product.list_schema import product_list_schema

@extend_schema_view(
    get=product_list_schema
)
class ProductListAPIView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = ProductListResponseSerializer
    pagination_class = ProductPagination

    # =====================================================
    # QUERYSET
    # =====================================================
    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        return ProductSelector.list_products(
            filters=self.request.query_params.dict(),
            user=user
        )