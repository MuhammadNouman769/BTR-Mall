# apps/products/validators/product_validator.py

from rest_framework.exceptions import ValidationError

from apps.products.models import (
    Category,
)

from apps.common.enums import (
    UserRoleChoices,
    ShopStatusChoices,
    SellerTrustLevel,
    ProductStatus,
)


class ProductValidator:

    ACTIVE_TRUST_LEVELS = {
        SellerTrustLevel.TRUSTED,
        SellerTrustLevel.VERIFIED,
    }

    # =====================================================
    # VALIDATE SELLER
    # =====================================================

    @staticmethod
    def validate_seller(user):

        if user.role != UserRoleChoices.SELLER:

            raise ValidationError({
                "error": "Only sellers can manage products."
            })

        if not hasattr(user, "shop"):

            raise ValidationError({
                "error": "Shop not found."
            })

        if (
            user.shop.shop_status !=
            ShopStatusChoices.APPROVED
        ):

            raise ValidationError({
                "error": "Your shop is not approved."
            })

        return user.shop

    # =====================================================
    # VALIDATE OWNER
    # =====================================================

    @staticmethod
    def validate_owner(product, user):

        if product.shop != user.shop:

            raise ValidationError({
                "error": "You do not own this product."
            })

    # =====================================================
    # VALIDATE CATEGORIES
    # =====================================================

    @staticmethod
    def validate_categories(categories):

        if not categories:
            return

        ids = [cat.id for cat in categories]

        db_categories = Category.objects.filter(
            id__in=ids
        )

        if db_categories.count() != len(ids):

            raise ValidationError({
                "categories": (
                    "One or more categories are invalid."
                )
            })

    # =====================================================
    # VALIDATE UPDATE
    # =====================================================

    @staticmethod
    def validate_update(instance):

        if instance.product_status in [

            ProductStatus.DELETED,

            ProductStatus.ARCHIVED,

        ]:

            raise ValidationError({
                "error": (
                    "This product cannot be updated."
                )
            })

    # =====================================================
    # DETERMINE STATUS
    # =====================================================

    @staticmethod
    def determine_status(shop, variants):

        total_stock = sum(

            variant.get(
                "stock_quantity",
                0
            )

            for variant in variants

        )

        if total_stock <= 0:

            return ProductStatus.OUT_OF_STOCK

        if (

            shop.trust_level
            in ProductValidator.ACTIVE_TRUST_LEVELS

        ):

            return ProductStatus.ACTIVE

        return ProductStatus.PENDING