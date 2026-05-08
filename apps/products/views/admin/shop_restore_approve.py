from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models.shop_restore_request import (
    ShopActionRequest,
    ShopRequestStatus
)

from apps.products.serializers.response.shop_restore_response import (
    ShopRestoreResponseSerializer
)

from apps.products.schemas.admin.restore_approve_schema import (
    shop_restore_approve_schema
)

from apps.common.enums import ShopStatusChoices


@extend_schema_view(
    post=shop_restore_approve_schema
)
class ApproveShopRestoreAPIView(APIView):

    permission_classes = [IsAdminUser]

    serializer_class = ShopRestoreResponseSerializer

    def post(self, request, id):

        try:
            request_obj = ShopActionRequest.objects.select_related(
                "shop",
                "reviewed_by"
            ).get(id=id)

        except ShopActionRequest.DoesNotExist:
            return Response(
                {
                    "error": "Restore request not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if request_obj.status != ShopRequestStatus.PENDING:
            return Response(
                {
                    "error": "This request has already been processed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        request_obj.status = ShopRequestStatus.APPROVED
        request_obj.reviewed_by = request.user
        request_obj.reviewed_at = timezone.now()
        request_obj.save()

        shop = request_obj.shop

        shop.restore()
        shop.shop_status = ShopStatusChoices.APPROVED
        shop.is_verified = True
        shop.rejection_reason = ""
        shop.verified_at = timezone.now()

        shop.save()

        return Response(
            {
                "message": "Shop restored successfully"
            },
            status=status.HTTP_200_OK
        )