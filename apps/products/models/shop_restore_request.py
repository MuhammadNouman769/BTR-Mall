from django.db import models
from django.conf import settings

from apps.utils.models import BaseModel
from apps.products.models.shop import Shop


class ShopActionType(models.TextChoices):
    RESTORE = "restore", "Restore"
    VERIFY = "verify", "Verify"
    REOPEN = "reopen", "Reopen"


class ShopRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class ShopActionRequest(BaseModel):

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="requests"
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    action_type = models.CharField(
        max_length=20,
        choices=ShopActionType.choices
    )

    status = models.CharField(
        max_length=20,
        choices=ShopRequestStatus.choices,
        default=ShopRequestStatus.PENDING
    )

    reason = models.TextField(blank=True)

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_shop_requests"
    )

    reviewed_at = models.DateTimeField(null=True, blank=True)

    admin_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.shop.name} - {self.action_type}"