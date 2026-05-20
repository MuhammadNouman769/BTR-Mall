from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

from apps.users.choices.role_choices import UserRoleChoices
from apps.users.choices.status_choices import UserStatusChoices


class UserManager(BaseUserManager):

    use_in_migrations = True

    # =====================================================
    # CREATE USER
    # =====================================================

    @transaction.atomic
    def create_user(
        self,
        email,
        password=None,
        **extra_fields
    ):

        if not email:
            raise ValueError(
                "Email is required"
            )

        if not extra_fields.get("phone"):
            raise ValueError(
                "Phone number is required"
            )

        email = self.normalize_email(email)

        # -------------------------------------------------
        # DEFAULT VALUES
        # -------------------------------------------------

        extra_fields.setdefault(
            "role",
            UserRoleChoices.CUSTOMER
        )

        extra_fields.setdefault(
            "account_status",
            UserStatusChoices.PENDING
        )

        extra_fields.setdefault(
            "is_active",
            False
        )

        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        user = self.model(
            email=email,
            **extra_fields
        )

        # -------------------------------------------------
        # PASSWORD
        # -------------------------------------------------

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    # =====================================================
    # CREATE SUPERUSER
    # =====================================================

    @transaction.atomic
    def create_superuser(
        self,
        email,
        password,
        **extra_fields
    ):

        extra_fields.setdefault(
            "role",
            UserRoleChoices.ADMIN
        )

        extra_fields.setdefault(
            "account_status",
            UserStatusChoices.ACTIVE
        )

        extra_fields.setdefault(
            "is_staff",
            True
        )

        extra_fields.setdefault(
            "is_superuser",
            True
        )

        extra_fields.setdefault(
            "is_active",
            True
        )

        # -------------------------------------------------
        # VALIDATIONS
        # -------------------------------------------------

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True"
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True"
            )

        return self.create_user(
            email,
            password,
            **extra_fields
        )

    # =====================================================
    # CREATE SELLER
    # =====================================================

    @transaction.atomic
    def create_seller(
        self,
        email,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault(
            "role",
            UserRoleChoices.SELLER
        )

        return self.create_user(
            email,
            password,
            **extra_fields
        )