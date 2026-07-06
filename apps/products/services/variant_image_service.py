# apps/products/services/variant_image_service.py

from django.db import transaction

from apps.products.models import VariantImage
from apps.products.validators.image_validator import (
    ImageValidator,
)


class VariantImageService:

    # =====================================================
    # CREATE SINGLE IMAGE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_image(
        user,
        validated_data,
    ):

        ImageValidator.validate_variant_image(
            validated_data,
        )

        return VariantImage.objects.create(
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

        image_data = {
            "image": validated_data.get(
                "image",
                instance.image,
            ),
            "is_main": validated_data.get(
                "is_main",
                instance.is_main,
            ),
        }

        ImageValidator.validate_variant_image(
            image_data,
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
        variant,
        images,
    ):

        if not images:
            return

        ImageValidator.validate_variant_images(
            images,
        )

        VariantImage.objects.bulk_create(
            [
                VariantImage(
                    variant=variant,
                    image=image["image"],
                    alt_text=image.get(
                        "alt_text",
                        "",
                    ),
                    is_main=image.get(
                        "is_main",
                        False,
                    ),
                    position=image.get(
                        "position",
                        index + 1,
                    ),
                )
                for index, image in enumerate(images)
            ]
        )

    # =====================================================
    # REPLACE ALL VARIANT IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_images(
        variant,
        images,
    ):

        if images is None:
            return

        ImageValidator.validate_variant_images(
            images,
        )

        variant.variant_images.all().delete()

        VariantImageService.create_images(
            variant,
            images,
        )

    # =====================================================
    # DELETE ALL VARIANT IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def delete_images(
        variant,
    ):

        variant.variant_images.all().delete()