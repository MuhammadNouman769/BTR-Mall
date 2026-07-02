

from django.db import transaction

from apps.products.models import ProductVariant
from apps.products.validators.product_validator import ProductValidator
from apps.products.validators.variant_validator import VariantValidator
from apps.products.services.variant_image_service import VariantImageService



class VariantService:
    # =====================================================
    # CREATE VARIANT
    # =====================================================
    @staticmethod
    @transaction.atomic
    def create_variant(user, validated_data):
        images = validated_data.pop("images", [])
        product = validated_data.get("product")
        ProductValidator.validate_owner(
            product,
            user,
        )
        VariantValidator.validate(
            [
                {
                    **validated_data,
                    "images": images,
                }
            ]
        )
        variant = ProductVariant.objects.create(
            **validated_data
        )
        VariantImageService.create_images(
            variant,
            images,
        )
        return variant

    # =====================================================
    # UPDATE VARIANT
    # =====================================================
    @staticmethod
    @transaction.atomic
    def update_variant(user, instance, validated_data):
        images = validated_data.pop("images", None)
        ProductValidator.validate_owner(
            instance.product,
            user,
        )
        if images is not None:
            VariantValidator.validate(
                [
                    {
                        **validated_data,
                        "images": images,
                    }
                ],
                product=instance.product,
            )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images is not None:
            VariantImageService.update_images(
                instance,
                images,
            )
        return instance

    # =====================================================
    # DELETE VARIANT
    # =====================================================
    @staticmethod
    @transaction.atomic
    def delete_variant(user, instance):
        ProductValidator.validate_owner(
            instance.product,
            user,
        )
        VariantImageService.delete_images(
            instance,
        )
        instance.delete()