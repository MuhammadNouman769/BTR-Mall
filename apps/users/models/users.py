from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from apps.utils.models import BaseModel

from ..choices.role_choices import UserRoleChoices
from ..choices.status_choices import UserStatusChoices
from ..managers.user_manager import UserManager


class User(AbstractUser, BaseModel):

    username = None

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone format: +923001234567"
    )

    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        db_index=True,
    )

    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,
        db_index=True,
    )

    profile_picture = models.ImageField(
        upload_to='users/profile/%Y/%m/',
        null=True,
        blank=True,
    )

    account_status = models.CharField(
        max_length=20,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.PENDING,
        db_index=True,
    )

    email_verified = models.BooleanField(default=False)

    phone_verified = models.BooleanField(default=False)

    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["account_status"]),
            models.Index(fields=["role", "account_status"]),
        ]

    def __str__(self):
        return self.email

    # =====================================================
    # ROLE HELPERS
    # =====================================================

    @property
    def is_customer(self):
        return self.role == UserRoleChoices.CUSTOMER

    @property
    def is_seller(self):
        return self.role == UserRoleChoices.SELLER

    @property
    def is_admin_user(self):
        return self.role == UserRoleChoices.ADMIN

    @property
    def is_staff_user(self):
        return self.role == UserRoleChoices.STAFF

    # =====================================================
    # STATUS HELPERS
    # =====================================================

    @property
    def is_active_account(self):
        return (
            self.account_status ==
            UserStatusChoices.ACTIVE
        )

    # =====================================================
    # SHOP HELPERS
    # =====================================================

    @property
    def has_shop(self):
        return hasattr(self, "shop")

    @property
    def is_seller_active(self):

        return (
            self.is_seller
            and self.email_verified
            and self.has_shop
            and self.shop.shop_status == "approved"
        )

    # =====================================================
    # USER HELPERS
    # =====================================================

    @property
    def full_name(self):
        return (
            f"{self.first_name} {self.last_name}"
        ).strip()