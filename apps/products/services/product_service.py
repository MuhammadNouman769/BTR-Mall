from django.db import transaction

from apps.products.models import Product

from apps.products.services.product_image_service import (
    ProductImageService,
)

from apps.products.validators.product_validator import (
    ProductValidator,
)


class ProductService:

    # =====================================================
    # CREATE PRODUCT
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_product(user, validated_data):

        ProductValidator.validate_create(
            user,
            validated_data,
        )

        images = validated_data.pop(
            "images",
            [],
        )

        categories = validated_data.pop(
            "categories",
            [],
        )

        # options aur variants apni APIs se create honge
        validated_data.pop("options", None)
        validated_data.pop("variants", None)

        product = Product.objects.create(
            shop=user.shop,
            **validated_data,
        )

        if categories:
            product.categories.set(categories)

        ProductImageService.create_images(
            product,
            images,
        )

        return product

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_product(
        user,
        instance,
        validated_data,
    ):

        ProductValidator.validate_update(
            user,
            instance,
            validated_data,
        )

        images = validated_data.pop(
            "images",
            None,
        )

        categories = validated_data.pop(
            "categories",
            None,
        )

        # options aur variants apni APIs se update honge
        validated_data.pop("options", None)
        validated_data.pop("variants", None)

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value,
            )

        instance.save()

        if categories is not None:
            instance.categories.set(
                categories,
            )

        ProductImageService.update_images(
            instance,
            images,
        )

        return instance

    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    @staticmethod
    @transaction.atomic
    def delete_product(user, instance):

        ProductValidator.validate_owner(
            user=user,
            product=instance,
        )

        instance.delete()