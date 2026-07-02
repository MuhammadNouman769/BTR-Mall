# apps/products/services/variant_image_service.py

from django.db import transaction

from apps.products.models import VariantImage

from apps.products.validators.image_validator import (
    ImageValidator,
)


class VariantImageService:

    # =====================================================
    # CREATE VARIANT IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_images(variant, images):

        if not images:
            return

        ImageValidator.validate_variant_images(
            images
        )

        VariantImage.objects.bulk_create([
            VariantImage(
                variant=variant,
                image=image["image"],
                alt_text=image.get("alt_text", ""),
                is_main=image.get("is_main", False),
                position=image.get("position", index + 1),
            )
            for index, image in enumerate(images)
        ])

    # =====================================================
    # UPDATE VARIANT IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_images(variant, images):

        if images is None:
            return

        ImageValidator.validate_variant_images(
            images
        )

        variant.variant_images.all().delete()

        VariantImageService.create_images(
            variant,
            images,
        )

    # =====================================================
    # DELETE VARIANT IMAGES
    # =====================================================

    @staticmethod
    @transaction.atomic
    def delete_images(variant):

        variant.variant_images.all().delete()