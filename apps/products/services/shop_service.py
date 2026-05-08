from apps.products.models import Shop
from apps.common.enums import ShopStatusChoices, UserRoleChoices
from rest_framework.exceptions import ValidationError


class ShopService:

    @staticmethod
    def create_shop(user, validated_data):

        if not user or not user.is_authenticated:
            raise ValidationError({
                "error": "Login required to create shop"
            })

        if user.role != UserRoleChoices.SELLER:
            raise ValidationError({
                "error": "Only sellers can create a shop"
            })

        # prevent duplicate shop
        if Shop.objects.filter(owner=user).exists():
            raise ValidationError({
                "error": "You already have a shop"
            })

        shop = Shop.objects.create(
            owner=user,
            shop_status=ShopStatusChoices.PENDING,
            is_verified=False,
            **validated_data
        )

        return shop

    @staticmethod
    def update_shop(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    @staticmethod
    def delete_shop(instance):
        instance.delete()