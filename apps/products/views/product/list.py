from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.products.selectors.product_selector import ProductSelector
from apps.products.serializers.response.product_response_serializers.product_response import ProductListResponseSerializer

from apps.products.pagination import ProductPagination
from apps.products.schemas.product.list_schema import product_list_schema


@product_list_schema
class ProductListAPIView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = ProductListResponseSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return ProductSelector.list_products(
            filters=self.request.query_params,
            user=self.request.user
        )