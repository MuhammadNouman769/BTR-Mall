# apps/products/services/product_service.py

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import (
    Product,
    ProductImage,
    ProductOption,
    ProductOptionValue,
    ProductVariant,
    Category,
    VariantImage,
)

from apps.common.enums import (
    ProductStatus,
    SellerTrustLevel,
    UserRoleChoices,
    ShopStatusChoices,
)


class ProductService:

    ACTIVE_TRUST_LEVELS = {
        SellerTrustLevel.TRUSTED,
        SellerTrustLevel.VERIFIED,
    }

    # =========================================================
    # VALIDATE SELLER
    # =========================================================
    @staticmethod
    def validate_seller(user):

        if user.role != UserRoleChoices.SELLER:
            raise ValidationError({
                "error": "Only sellers can manage products"
            })

        if not hasattr(user, "shop"):
            raise ValidationError({
                "error": "Shop not found"
            })

        if user.shop.shop_status != ShopStatusChoices.APPROVED:
            raise ValidationError({
                "error": "Shop is not approved"
            })

        return user.shop

    # =========================================================
    # VALIDATE PRODUCT OWNER
    # =========================================================
    @staticmethod
    def validate_product_owner(product, user):

        if product.shop != user.shop:
            raise ValidationError({
                "error": "You do not own this product"
            })

    # =========================================================
    # VALIDATE CATEGORIES
    # =========================================================
    @staticmethod
    def validate_categories(category_ids):

        if not category_ids:
            return []

        categories = Category.objects.filter(
            id__in=category_ids
        )

        if len(category_ids) != categories.count():
            raise ValidationError({
                "error": "Invalid categories provided"
            })

        return categories

    # =========================================================
    # VALIDATE PRODUCT IMAGES
    # =========================================================
    @staticmethod
    def validate_images(images):

        if len(images) > 10:
            raise ValidationError({
                "error": "Maximum 10 product images allowed"
            })

        for img in images:

            if not img.get("image"):
                raise ValidationError({
                    "error": "Image file is required"
                })

    # =========================================================
    # VALIDATE OPTIONS
    # =========================================================
    @staticmethod
    def validate_options(options):

        option_names = set()

        for opt in options:

            name = opt["name"].strip().lower()

            if name in option_names:
                raise ValidationError({
                    "error": f'Duplicate option "{name}"'
                })

            option_names.add(name)

            values = opt.get("values", [])

            if not values:
                raise ValidationError({
                    "error": f'Option "{name}" must contain values'
                })

            value_names = set()

            for value in values:

                val = (
                    value["value"]
                    if isinstance(value, dict)
                    else value
                ).strip().lower()

                if val in value_names:
                    raise ValidationError({
                        "error": f'Duplicate value "{val}" in option "{name}"'
                    })

                value_names.add(val)

    # =========================================================
    # VALIDATE VARIANTS
    # =========================================================
    @staticmethod
    def validate_variants(variants, product=None):

        if not variants:
            raise ValidationError({
                "error": "At least one variant is required"
            })

        skus = set()

        for var in variants:

            sku = var.get("sku")
            price = var.get("price", 0)
            stock = var.get("stock_quantity", 0)

            if not sku:
                raise ValidationError({
                    "error": "SKU is required"
                })

            if sku in skus:
                raise ValidationError({
                    "error": f'Duplicate SKU "{sku}"'
                })

            existing_variant = ProductVariant.objects.filter(
                sku=sku
            )

            if product:
                existing_variant = existing_variant.exclude(
                    product=product
                )

            if existing_variant.exists():
                raise ValidationError({
                    "error": f'SKU "{sku}" already exists'
                })

            if price <= 0:
                raise ValidationError({
                    "error": "Variant price must be greater than 0"
                })

            if stock < 0:
                raise ValidationError({
                    "error": "Stock quantity cannot be negative"
                })

            images = var.get("images", [])

            if len(images) > 5:
                raise ValidationError({
                    "error": "Maximum 5 variant images allowed"
                })

            main_images = [
                img for img in images
                if img.get("is_main")
            ]

            if len(main_images) > 1:
                raise ValidationError({
                    "error": "Only one main image allowed per variant"
                })

            skus.add(sku)

    # =========================================================
    # DETERMINE PRODUCT STATUS
    # =========================================================
    @staticmethod
    def determine_product_status(shop, variants):

        total_stock = sum(
            var.get("stock_quantity", 0)
            for var in variants
        )

        if total_stock <= 0:
            return ProductStatus.OUT_OF_STOCK

        if shop.trust_level in ProductService.ACTIVE_TRUST_LEVELS:
            return ProductStatus.ACTIVE

        return ProductStatus.PENDING

    # =========================================================
    # CREATE PRODUCT OPTIONS
    # =========================================================
    @staticmethod
    def create_options(product, options):

        option_objects = []

        for opt in options:

            option = ProductOption.objects.create(
                product=product,
                name=opt["name"]
            )

            option_objects.append(option)

            values = opt.get("values", [])

            ProductOptionValue.objects.bulk_create([
                ProductOptionValue(
                    option=option,
                    value=v if isinstance(v, str) else v["value"]
                )
                for v in values
            ])

        return option_objects

    # =========================================================
    # CREATE PRODUCT VARIANTS
    # =========================================================
    @staticmethod
    def create_variants(product, variants):

        for var in variants:

            variant_data = var.copy()

            images = variant_data.pop("images", [])

            variant = ProductVariant.objects.create(
                product=product,
                **variant_data
            )

            variant_images = []

            for img in images:

                variant_images.append(
                    VariantImage(
                        variant=variant,
                        image=img["image"],
                        alt_text=img.get("alt_text", ""),
                        is_main=img.get("is_main", False),
                        position=img.get("position", 0),
                    )
                )

            if variant_images:
                VariantImage.objects.bulk_create(
                    variant_images
                )

    # =========================================================
    # CREATE PRODUCT
    # =========================================================
    @staticmethod
    @transaction.atomic
    def create_product(user, validated_data):

        shop = ProductService.validate_seller(user)

        images = validated_data.pop("images", [])
        options = validated_data.pop("options", [])
        variants = validated_data.pop("variants", [])
        category_ids = validated_data.pop("category_ids", [])

        # -----------------------------------------------------
        # VALIDATIONS
        # -----------------------------------------------------
        categories = validated_data.pop("categories", [])
        if categories:
            product.categories.set(categories)

        ProductService.validate_images(images)

        ProductService.validate_options(options)

        ProductService.validate_variants(variants)

        # -----------------------------------------------------
        # DETERMINE STATUS
        # -----------------------------------------------------
        product_status = ProductService.determine_product_status(
            shop,
            variants
        )

        # -----------------------------------------------------
        # CREATE PRODUCT
        # -----------------------------------------------------
        product = Product.objects.create(
            shop=shop,
            product_status=product_status,
            **validated_data
        )

        # -----------------------------------------------------
        # CATEGORIES
        # -----------------------------------------------------
        if categories:
            product.categories.set(categories)

        # -----------------------------------------------------
        # PRODUCT IMAGES
        # -----------------------------------------------------
        if images:

            ProductImage.objects.bulk_create([
                ProductImage(
                    product=product,
                    image=img["image"],
                    alt_text=img.get("alt_text", ""),
                    position=img.get("position", 0),
                )
                for img in images
            ])

        # -----------------------------------------------------
        # OPTIONS
        # -----------------------------------------------------
        if options:

            ProductService.create_options(
                product,
                options
            )

        # -----------------------------------------------------
        # VARIANTS
        # -----------------------------------------------------
        if variants:

            ProductService.create_variants(
                product,
                variants
            )

        return product

    # =========================================================
    # UPDATE PRODUCT
    # =========================================================
    @staticmethod
    @transaction.atomic
    def update_product(instance, validated_data):

        if instance.product_status in [
            ProductStatus.DELETED,
            ProductStatus.ARCHIVED,
        ]:
            raise ValidationError({
                "error": "This product cannot be updated"
            })

        images = validated_data.pop("images", None)
        options = validated_data.pop("options", None)
        variants = validated_data.pop("variants", None)
        category_ids = validated_data.pop("category_ids", None)

        # -----------------------------------------------------
        # BASIC FIELDS UPDATE
        # -----------------------------------------------------
        update_fields = []

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

            update_fields.append(attr)

        if update_fields:
            instance.save(update_fields=update_fields)

        # -----------------------------------------------------
        # UPDATE CATEGORIES
        # -----------------------------------------------------
        if category_ids is not None:

            categories = ProductService.validate_categories(
                category_ids
            )

            instance.categories.set(categories)

        # -----------------------------------------------------
        # UPDATE IMAGES
        # -----------------------------------------------------
        if images is not None:

            ProductService.validate_images(images)

            instance.images.all().delete()

            ProductImage.objects.bulk_create([
                ProductImage(
                    product=instance,
                    image=img["image"],
                    alt_text=img.get("alt_text", ""),
                    position=img.get("position", 0),
                )
                for img in images
            ])

        # -----------------------------------------------------
        # UPDATE OPTIONS
        # -----------------------------------------------------
        if options is not None:

            ProductService.validate_options(options)

            instance.options.all().delete()

            ProductService.create_options(
                instance,
                options
            )

        # -----------------------------------------------------
        # UPDATE VARIANTS
        # -----------------------------------------------------
        if variants is not None:

            ProductService.validate_variants(
                variants,
                product=instance
            )

            instance.variants.all().delete()

            ProductService.create_variants(
                instance,
                variants
            )

            instance.product_status = (
                ProductService.determine_product_status(
                    instance.shop,
                    variants
                )
            )

            instance.save(
                update_fields=["product_status"]
            )

        return instance

    # =========================================================
    # SOFT DELETE PRODUCT
    # =========================================================
    @staticmethod
    def delete_product(instance):

        instance.product_status = ProductStatus.DELETED

        instance.save(
            update_fields=["product_status"]
        )

    # =========================================================
    # ACTIVATE PRODUCT
    # =========================================================
    @staticmethod
    def activate_product(instance):

        instance.product_status = ProductStatus.ACTIVE

        instance.save(
            update_fields=["product_status"]
        )

    # =========================================================
    # ARCHIVE PRODUCT
    # =========================================================
    @staticmethod
    def archive_product(instance):

        instance.product_status = ProductStatus.ARCHIVED

        instance.save(
            update_fields=["product_status"]
        )

    # =========================================================
    # MARK OUT OF STOCK
    # =========================================================
    @staticmethod
    def mark_out_of_stock(instance):

        instance.product_status = ProductStatus.OUT_OF_STOCK

        instance.save(
            update_fields=["product_status"]
        )