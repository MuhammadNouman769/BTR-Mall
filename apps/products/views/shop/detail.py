from rest_framework.generics import RetrieveAPIView

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.shop_selector import (
    ShopSelector
)

from apps.products.serializers.response.shop_create_response_serializers.shop_response import (
    ShopDetailSerializer
)

from apps.products.schemas.shop.detail_schema import (
    shop_detail_schema
)


@extend_schema_view(
    get=shop_detail_schema
)
class ShopDetailAPIView(RetrieveAPIView):

    serializer_class = ShopDetailSerializer

    lookup_field = "pk"

    def get_queryset(self):

        return ShopSelector.base_queryset()