from rest_framework.exceptions import ValidationError

from apps.products.models import ProductVariant

from apps.products.validators.image_validator import (
    ImageValidator,
)


class VariantValidator:

    # =====================================================
    # VALIDATE VARIANTS
    # =====================================================

    @staticmethod
    def validate(variants, product=None):

        if not variants:

            raise ValidationError({
                "variants": (
                    "At least one variant is required."
                )
            })

        skus = set()

        for variant in variants:

            sku = variant.get("sku")
            price = variant.get("price")
            stock = variant.get("stock_quantity", 0)

            # ==========================================
            # SKU
            # ==========================================

            if not sku:

                raise ValidationError({
                    "sku": "SKU is required."
                })

            if sku in skus:

                raise ValidationError({
                    "sku": (
                        f'Duplicate SKU "{sku}".'
                    )
                })

            queryset = ProductVariant.objects.filter(
                sku=sku
            )

            if product:

                queryset = queryset.exclude(
                    product=product
                )

            if queryset.exists():

                raise ValidationError({
                    "sku": (
                        f'SKU "{sku}" already exists.'
                    )
                })

            skus.add(sku)

            # ==========================================
            # PRICE
            # ==========================================

            if price is None:

                raise ValidationError({
                    "price": "Price is required."
                })

            if price <= 0:

                raise ValidationError({
                    "price": (
                        "Price must be greater than 0."
                    )
                })

            # ==========================================
            # STOCK
            # ==========================================

            if stock < 0:

                raise ValidationError({
                    "stock_quantity": (
                        "Stock cannot be negative."
                    )
                })

            # ==========================================
            # IMAGES
            # ==========================================

            ImageValidator.validate_variant_images(
                variant.get("images", [])
            )