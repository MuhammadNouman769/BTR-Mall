from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import Shop
from apps.common.enums import (
    ShopStatusChoices,
    UserRoleChoices
)


class ShopService:

    # =========================================================
    # VALIDATE SELLER
    # =========================================================
    @staticmethod
    def validate_seller(user):

        if not user or not user.is_authenticated:
            raise ValidationError({
                "error": "Authentication required"
            })

        if user.role != UserRoleChoices.SELLER:
            raise ValidationError({
                "error": "Only sellers can create shops"
            })

    # =========================================================
    # CHECK EXISTING SHOP
    # =========================================================
    @staticmethod
    def validate_existing_shop(user):

        if Shop.objects.filter(owner=user).exists():
            raise ValidationError({
                "error": "You already have a shop"
            })

    # =========================================================
    # CREATE SHOP
    # =========================================================
    @staticmethod
    @transaction.atomic
    def create_shop(user, validated_data):

        ShopService.validate_seller(user)

        ShopService.validate_existing_shop(user)

        shop = Shop.objects.create(
            owner=user,
            shop_status=ShopStatusChoices.PENDING,
            is_verified=False,
            **validated_data
        )

        return shop

    # =========================================================
    # UPDATE SHOP
    # =========================================================
    @staticmethod
    @transaction.atomic
    def update_shop(instance, validated_data):

        immutable_fields = [
            "owner",
            "shop_status",
            "is_verified",
            "rating",
        ]

        for field in immutable_fields:
            validated_data.pop(field, None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    # =========================================================
    # DELETE SHOP
    # =========================================================
    @staticmethod
    def delete_shop(instance):

        instance.delete()