from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.products.models import Shop
from apps.products.serializers.response.shop_create_response_serializers.shop_response import ShopDetailSerializer

from apps.products.serializers.response.admin_approvel_response_serializers.shop_trash_response import ShopTrashSerializer

from drf_spectacular.utils import extend_schema_view, extend_schema
from apps.products.schemas.admin_aprrovel.shop_trash_schema import (
    shop_trash_schema
)
@extend_schema_view(
    get=shop_trash_schema
)
class ShopTrashListAPIView(APIView):
    
    permission_classes = [IsAdminUser]
    serializer_class = ShopTrashSerializer

    def get(self, request):
        shops = Shop.all_objects.filter(is_deleted=True)

        return Response({
            "count": shops.count(),
            "data": ShopTrashSerializer(shops, many=True).data
        })