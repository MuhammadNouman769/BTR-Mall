from rest_framework.exceptions import ValidationError

from apps.products.models import Shop
from apps.products.models.shop_restore_request import (
    ShopActionRequest,
    ShopActionType,
    ShopRequestStatus,
)


class ShopRestoreService:

    @staticmethod
    def create_restore_request(user, shop, reason=""):

        if not shop.is_deleted:
            raise ValidationError({
                "error": "Shop is already active"
            })

        existing = ShopActionRequest.objects.filter(
            shop=shop,
            action_type=ShopActionType.RESTORE,
            status=ShopRequestStatus.PENDING
        ).exists()

        if existing:
            raise ValidationError({
                "error": "Restore request already pending"
            })

        return ShopActionRequest.objects.create(
            shop=shop,
            requested_by=user,
            action_type=ShopActionType.RESTORE,
            reason=reason
        )