from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.shop_selector import ShopSelector

from apps.products.services.shop_service import (
    ShopService
)

from apps.products.serializers.request.shop_create_request_serializers.shop_update import (
    ShopUpdateSerializer
)

from apps.products.serializers.response.shop_create_response_serializers.shop_response import (
    ShopDetailSerializer
)

from apps.products.schemas.shop.update_schema import (
    shop_update_schema
)


@extend_schema_view(
    patch=shop_update_schema
)
class ShopUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ShopUpdateSerializer

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def patch(self, request):

        shop = ShopSelector.user_shop(
            request.user
        )

        serializer = ShopUpdateSerializer(
            shop,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        shop = ShopService.update_shop(
            instance=shop,
            validated_data=serializer.validated_data
        )

        return Response({
            "message": "Shop updated successfully",
            "data": ShopDetailSerializer(shop).data
        })