from rest_framework.exceptions import ValidationError
from apps.products.models import Product
from apps.users.choices.role_choices import UserRoleChoices
from apps.products.choices.shop_status_choices import ShopStatusChoices


class ProductService:

    @staticmethod
    def validate_seller(user):
        if user.role != UserRoleChoices.SELLER:
            raise ValidationError({"error": "Only sellers can create products"})

        if not hasattr(user, "shop"):
            raise ValidationError({"error": "Shop not found"})

        if user.shop.shop_status != ShopStatusChoices.APPROVED:
            raise ValidationError({"error": "Shop not approved"})

        return user.shop

    @staticmethod
    def create_product(user, validated_data):
        shop = ProductService.validate_seller(user)

        validated_data.pop("shop", None)

        return Product.objects.create(
            shop=shop,
            **validated_data
        )