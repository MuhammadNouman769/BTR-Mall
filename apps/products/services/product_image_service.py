from django.db import transaction

from apps.products.models import ProductImage

from apps.products.validators.image_validator import (
    ImageValidator,
)


class ProductImageService:

    # =====================================================
    # CREATE SINGLE IMAGE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_image(user, validated_data):

        ImageValidator.validate_product_images(
            [validated_data]
        )

        return ProductImage.objects.create(
            **validated_data,
        )

    # =====================================================
    # UPDATE SINGLE IMAGE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_image(
        user,
        instance,
        validated_data,
    ):

        ImageValidator.validate_product_images(
            [validated_data]
        )

        for field, value in validated_data.items():

            setattr(
                instance,
                field,
                value,
            )

        instance.save()

        return instance

    # =====================================================
    # DELETE SINGLE IMAGE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def delete_image(
        user,
        instance,
    ):

        instance.delete()

    # =====================================================
    # CREATE MULTIPLE IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_images(
        product,
        images,
    ):

        if not images:
            return

        ImageValidator.validate_product_images(
            images,
        )

        ProductImage.objects.bulk_create(
            [
                ProductImage(
                    product=product,
                    image=image["image"],
                    alt_text=image.get(
                        "alt_text",
                        "",
                    ),
                    position=image.get(
                        "position",
                        0,
                    ),
                )
                for image in images
            ]
        )

    # =====================================================
    # UPDATE MULTIPLE IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_images(
        product,
        images,
    ):

        if images is None:
            return

        product.images.all().delete()

        ProductImageService.create_images(
            product,
            images,
        )