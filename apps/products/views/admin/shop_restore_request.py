from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.products.models.shop_restore_request import ShopActionRequest, ShopActionType
from apps.products.serializers.response.shop_restore_request_list import (
    ShopRestoreRequestListSerializer
)


class ShopRestoreRequestListAPIView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ShopRestoreRequestListSerializer

    def get_queryset(self):
        return ShopActionRequest.objects.filter(
            action_type=ShopActionType.RESTORE
        ).select_related("shop", "requested_by").order_by("-created_at")