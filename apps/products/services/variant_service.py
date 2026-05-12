from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import ProductVariant, VariantImage


class VariantService:

    # =========================================================
    #                     CREATE VARIANT
    # =========================================================
    @staticmethod
    @transaction.atomic
    def create_variant(user, validated_data):

        images_data = validated_data.pop("images", [])

        product = validated_data.get("product")

        # =========================================
        #          OWNERSHIP VALIDATION
        # =========================================
        if product.shop.owner != user:
            raise ValidationError({
                "error": "You cannot add variants to this product"
            })

        # =========================================
        #          MAIN IMAGE VALIDATION
        # =========================================
        main_images_count = sum(
            1 for img in images_data if img.get("is_main")
        )

        if main_images_count > 1:
            raise ValidationError({
                "error": "Only one main image is allowed"
            })

        # =========================================
        #            CREATE VARIANT
        # =========================================
        variant = ProductVariant.objects.create(
            **validated_data
        )

        # =========================================
        #             CREATE IMAGES
        # =========================================
        variant_images = []

        for index, img in enumerate(images_data):

            variant_images.append(
                VariantImage(
                    variant=variant,
                    image=img["image"],
                    alt_text=img.get("alt_text", ""),
                    is_main=img.get("is_main", False),
                    position=index + 1
                )
            )

        VariantImage.objects.bulk_create(variant_images)

        return variant
    # =========================================================
    #                     UPDATE VARIANT
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update_variant(user, instance, validated_data):

        images_data = validated_data.pop("images", None)

        # =========================================
        #          OWNERSHIP VALIDATION
        # =========================================
        if instance.product.shop.owner != user:
            raise ValidationError({
                "error": "You cannot update this variant"
            })

        # =========================================
        #          UPDATE FIELDS
        # =========================================
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # =========================================
        #          UPDATE IMAGES
        # =========================================
        if images_data is not None:

            main_images_count = sum(
                1 for img in images_data if img.get("is_main")
            )

            if main_images_count > 1:
                raise ValidationError({
                    "error": "Only one main image is allowed"
                })

            # old images remove
            instance.variant_images.all().delete()

            # bulk create new images
            variant_images = []

            for index, img in enumerate(images_data):

                variant_images.append(
                    VariantImage(
                        variant=instance,
                        image=img["image"],
                        alt_text=img.get("alt_text", ""),
                        is_main=img.get("is_main", False),
                        position=index + 1
                    )
                )

            VariantImage.objects.bulk_create(
                variant_images
            )

        return instance

    # =========================================================
    #                    DELETE VARIANT
    # =========================================================
    @staticmethod
    @transaction.atomic
    def delete_variant(user, instance):

        # =========================================
        #          OWNERSHIP VALIDATION
        # =========================================
        if instance.product.shop.owner != user:
            raise ValidationError({
                "error": "You cannot delete this variant"
            })

        instance.delete()