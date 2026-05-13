from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.products.models import Shop
from apps.products.serializers.response.admin_approvel_response_serializers.shop_hard_delete_response import ShopHardDeleteResponseSerializer

from drf_spectacular.utils import extend_schema_view, extend_schema
from apps.products.schemas.admin_aprrovel.shop_hard_delete_schema import (
    shop_hard_delete_schema
)
@extend_schema_view(
    delete=shop_hard_delete_schema
)   
class AdminShopHardDeleteAPIView(APIView):
    
    permission_classes = [IsAdminUser]
    serializer_class = ShopHardDeleteResponseSerializer

    def delete(self, request, id):

        shop = Shop.all_objects.filter(id=id).first()

        if not shop:
            return Response({"error": "Shop not found"}, status=404)

        shop.hard_delete()

        return Response({
            "message": "Shop permanently deleted",
            "id": shop.id
        })