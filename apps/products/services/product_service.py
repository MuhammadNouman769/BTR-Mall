# services/product_service.py

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import (
    Product,
    ProductImage,
    ProductOption,
    ProductOptionValue,
    ProductVariant,
    Category
)

from apps.common.enums import (
    ProductStatus,
    SellerTrustLevel,
    UserRoleChoices,
    ShopStatusChoices
)


class ProductService:

    # =========================================================
    # VALIDATE SELLER
    # =========================================================
    @staticmethod
    def validate_seller(user):

        if user.role != UserRoleChoices.SELLER:
            raise ValidationError({
                "error": "Only sellers can create products"
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
    # VALIDATE CATEGORIES
    # =========================================================
    @staticmethod
    def validate_categories(category_ids):

        categories = Category.objects.filter(
            id__in=category_ids
        )

        if len(category_ids) != categories.count():
            raise ValidationError({
                "error": "Invalid categories provided"
            })

        return categories

    # =========================================================
    # VALIDATE IMAGES
    # =========================================================
    @staticmethod
    def validate_images(images):

        if len(images) > 10:
            raise ValidationError({
                "error": "Maximum 10 images allowed"
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

    # =========================================================
    # VALIDATE VARIANTS
    # =========================================================
    @staticmethod
    def validate_variants(variants):

        if not variants:
            raise ValidationError({
                "error": "At least one variant is required"
            })

        skus = set()

        for var in variants:

            price = var.get("price", 0)
            stock = var.get("stock_quantity", 0)
            sku = var.get("sku")

            if price <= 0:
                raise ValidationError({
                    "error": "Variant price must be greater than 0"
                })

            if stock < 0:
                raise ValidationError({
                    "error": "Stock quantity cannot be negative"
                })

            if sku in skus:
                raise ValidationError({
                    "error": f'Duplicate SKU "{sku}"'
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

        trust_level = getattr(
            shop,
            "trust_level",
            SellerTrustLevel.NEW
        )

        if trust_level == SellerTrustLevel.TRUSTED:
            return ProductStatus.ACTIVE

        if trust_level == SellerTrustLevel.VERIFIED:
            return ProductStatus.ACTIVE

        return ProductStatus.PENDING

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

        # ---------------- VALIDATIONS ----------------
        categories = ProductService.validate_categories(category_ids)

        ProductService.validate_images(images)

        ProductService.validate_options(options)

        ProductService.validate_variants(variants)

        # ---------------- PRODUCT STATUS ----------------
        product_status = ProductService.determine_product_status(
            shop,
            variants
        )

        # ---------------- CREATE PRODUCT ----------------
        product = Product.objects.create(
            shop=shop,
            product_status=product_status,
            **validated_data
        )

        # ---------------- CATEGORIES ----------------
        product.categories.set(categories)

        # ---------------- PRODUCT IMAGES ----------------
        if images:

            ProductImage.objects.bulk_create([
                ProductImage(
                    product=product,
                    **img
                )
                for img in images
            ])

        # ---------------- OPTIONS + VALUES ----------------
        if options:

            for opt in options:

                option_obj = ProductOption.objects.create(
                    product=product,
                    name=opt["name"]
                )

                values = opt.get("values", [])

                ProductOptionValue.objects.bulk_create([
                    ProductOptionValue(
                        option=option_obj,
                        value=v["value"] if isinstance(v, dict) else v
                    )
                    for v in values
                ])

        # ---------------- VARIANTS ----------------
        ProductVariant.objects.bulk_create([
            ProductVariant(
                product=product,
                **var
            )
            for var in variants
        ])

        return product

    # =========================================================
    # UPDATE PRODUCT
    # =========================================================
    @staticmethod
    @transaction.atomic
    def update_product(instance, validated_data):

        if instance.product_status == ProductStatus.DELETED:
            raise ValidationError({
                "error": "Deleted product cannot be updated"
            })

        if instance.product_status == ProductStatus.ARCHIVED:
            raise ValidationError({
                "error": "Archived product cannot be updated"
            })

        images = validated_data.pop("images", None)
        options = validated_data.pop("options", None)
        variants = validated_data.pop("variants", None)
        category_ids = validated_data.pop("category_ids", None)

        # ---------------- BASIC FIELDS ----------------
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # ---------------- CATEGORIES ----------------
        if category_ids is not None:

            categories = ProductService.validate_categories(
                category_ids
            )

            instance.categories.set(categories)

        # ---------------- IMAGES ----------------
        if images is not None:

            ProductService.validate_images(images)

            instance.images.all().delete()

            ProductImage.objects.bulk_create([
                ProductImage(
                    product=instance,
                    **img
                )
                for img in images
            ])

        # ---------------- OPTIONS ----------------
        if options is not None:

            ProductService.validate_options(options)

            instance.options.all().delete()

            for opt in options:

                option = ProductOption.objects.create(
                    product=instance,
                    name=opt["name"]
                )

                values = opt.get("values", [])

                ProductOptionValue.objects.bulk_create([
                    ProductOptionValue(
                        option=option,
                        value=v["value"] if isinstance(v, dict) else v
                    )
                    for v in values
                ])

        # ---------------- VARIANTS ----------------
        if variants is not None:

            ProductService.validate_variants(variants)

            instance.variants.all().delete()

            ProductVariant.objects.bulk_create([
                ProductVariant(
                    product=instance,
                    **var
                )
                for var in variants
            ])

            # auto status update
            instance.product_status = (
                ProductService.determine_product_status(
                    instance.shop,
                    variants
                )
            )

            instance.save()

        return instance

    # =========================================================
    # SOFT DELETE PRODUCT
    # =========================================================
    @staticmethod
    def delete_product(instance):

        instance.product_status = ProductStatus.DELETED

        instance.save()

    # =========================================================
    # ACTIVATE PRODUCT
    # =========================================================
    @staticmethod
    def activate_product(instance):

        instance.product_status = ProductStatus.ACTIVE

        instance.save()

    # =========================================================
    # ARCHIVE PRODUCT
    # =========================================================
    @staticmethod
    def archive_product(instance):

        instance.product_status = ProductStatus.ARCHIVED

        instance.save()

    # =========================================================
    # MARK OUT OF STOCK
    # =========================================================
    @staticmethod
    def mark_out_of_stock(instance):

        instance.product_status = ProductStatus.OUT_OF_STOCK

        instance.save()