from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from apps.products.models import Shop
from apps.products.services.shop_service import ShopService
from apps.products.serializers.request.shop_update import ShopUpdateSerializer
from apps.products.serializers.response.shop_response import ShopDetailSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(request=ShopUpdateSerializer, responses=ShopDetailSerializer)
class ShopUpdateAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, *args, **kwargs):

        try:
            shop = request.user.shop
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found"}, status=404)

        serializer = ShopUpdateSerializer(
            shop,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        shop = ShopService.update_shop(shop, serializer.validated_data)

        return Response({
            "message": "Shop updated successfully",
            "data": ShopDetailSerializer(shop).data
        })