from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from apps.products.models.shop_restore_request import ShopActionRequest
from apps.products.serializers.request.admin_approvel_request_serializers.shop_restore_request_list import ShopRestoreRequestListSerializer


class ShopRestoreRequestDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ShopRestoreRequestListSerializer
    queryset = ShopActionRequest.objects.all()
    lookup_field = "id"