from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.serializers.request.shop_create_request_serializers.shop_create import (
    ShopCreateSerializer
)

from apps.products.services.shop_service import ShopService

from apps.products.schemas.shop.create_schema import (
    shop_create_schema
)


@extend_schema_view(
    post=shop_create_schema
)
class ShopCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ShopCreateSerializer

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def post(self, request):

        serializer = ShopCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        shop = ShopService.create_shop(
            user=request.user,
            validated_data=serializer.validated_data
        )

        return Response(
            {
                "message": "Shop created successfully",
                "id": shop.id
            },
            status=status.HTTP_201_CREATED
        )