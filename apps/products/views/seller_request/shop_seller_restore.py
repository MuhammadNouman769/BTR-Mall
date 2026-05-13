from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import Shop
from apps.products.models.shop_restore_request import (
    ShopActionRequest,
    ShopRequestStatus
)

from apps.products.serializers.request.admin_approvel_request_serializers.shop_restore_request import (
    SellerShopRestoreRequestSerializer
)

from apps.products.serializers.response.admin_approvel_response_serializers.shop_restore_response import (
    SellerShopRestoreResponseSerializer
)

from apps.products.services.shop_restore_service import (
    ShopRestoreService
)

from apps.products.schemas.seller_request.restore_request_schema import (
    shop_restore_request_schema
)


@extend_schema_view(
    post=shop_restore_request_schema
)
class ShopRestoreRequestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = SellerShopRestoreRequestSerializer

    def post(self, request, id):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            shop = Shop.all_objects.get(
                id=id,
                owner=request.user
            )

        except Shop.DoesNotExist:
            return Response(
                {
                    "error": "Shop not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not shop.is_deleted:
            return Response(
                {
                    "error": "Shop is already active"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        pending_request_exists = ShopActionRequest.objects.filter(
            shop=shop,
            status=ShopRequestStatus.PENDING
        ).exists()

        if pending_request_exists:
            return Response(
                {
                    "error": "Restore request already submitted"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ShopRestoreService.create_restore_request(
            user=request.user,
            shop=shop,
            reason=serializer.validated_data.get("reason", "")
        )

        return Response(
            {
                "message": "Restore request submitted successfully"
            },
            status=status.HTTP_200_OK
        )