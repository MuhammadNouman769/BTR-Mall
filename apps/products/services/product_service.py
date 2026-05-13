from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import (
    Product,
    ProductImage,
    ProductOption,
    ProductOptionValue,
    ProductVariant,
    Category,
    VariantImage
)

from apps.common.enums import (
    ProductStatus,
    SellerTrustLevel,
    UserRoleChoices,
    ShopStatusChoices
)


class ProductService:

    # =========================================================
    # SELLER VALIDATION
    # =========================================================
    @staticmethod
    def validate_seller(user):
        if user.role != UserRoleChoices.SELLER:
            raise ValidationError({"error": "Only sellers can create products"})

        if not hasattr(user, "shop"):
            raise ValidationError({"error": "Shop not found"})

        if user.shop.shop_status != ShopStatusChoices.APPROVED:
            raise ValidationError({"error": "Shop is not approved"})

        return user.shop

    # =========================================================
    # CATEGORY VALIDATION
    # =========================================================
    @staticmethod
    def validate_categories(category_ids):
        categories = Category.objects.filter(id__in=category_ids)

        if len(category_ids) != categories.count():
            raise ValidationError({"error": "Invalid categories provided"})

        return categories

    # =========================================================
    # IMAGE VALIDATION
    # =========================================================
    @staticmethod
    def validate_images(images):
        if len(images) > 10:
            raise ValidationError({"error": "Maximum 10 images allowed"})

    # =========================================================
    # OPTION VALIDATION
    # =========================================================
    @staticmethod
    def validate_options(options):
        names = set()

        for opt in options:
            name = opt["name"].strip().lower()

            if name in names:
                raise ValidationError({"error": f"Duplicate option {name}"})

            names.add(name)

            if not opt.get("values"):
                raise ValidationError({"error": f"Option {name} must have values"})

    # =========================================================
    # VARIANT VALIDATION
    # =========================================================
    @staticmethod
    def validate_variants(variants):
        if not variants:
            raise ValidationError({"error": "At least one variant required"})

        skus = set()

        for var in variants:
            sku = var.get("sku")
            price = var.get("price", 0)
            stock = var.get("stock_quantity", 0)

            if not sku:
                raise ValidationError({"error": "SKU is required"})

            if sku in skus:
                raise ValidationError({"error": f"Duplicate SKU {sku}"})

            if price <= 0:
                raise ValidationError({"error": "Price must be greater than 0"})

            if stock < 0:
                raise ValidationError({"error": "Stock cannot be negative"})

            skus.add(sku)

    # =========================================================
    # PRODUCT STATUS LOGIC
    # =========================================================
    @staticmethod
    def determine_product_status(shop, variants):
        total_stock = sum(v.get("stock_quantity", 0) for v in variants)

        if total_stock <= 0:
            return ProductStatus.OUT_OF_STOCK

        if shop.trust_level in [
            SellerTrustLevel.TRUSTED,
            SellerTrustLevel.VERIFIED
        ]:
            return ProductStatus.ACTIVE

        return ProductStatus.PENDING

    # =========================================================
    # VARIANT CREATION (CLEAN)
    # =========================================================
    @staticmethod
    def create_variants(product, variants):
        for var in variants:
            images = var.pop("images", [])

            variant = ProductVariant.objects.create(
                product=product,
                **var
            )

            for img in images:
                VariantImage.objects.create(
                    variant=variant,
                    image=img["image"],
                    alt_text=img.get("alt_text", ""),
                    is_main=img.get("is_main", False),
                    position=img.get("position", 0),
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

        # VALIDATIONS
        categories = ProductService.validate_categories(category_ids)
        ProductService.validate_images(images)
        ProductService.validate_options(options)
        ProductService.validate_variants(variants)

        # STATUS
        status = ProductService.determine_product_status(shop, variants)

        # CREATE PRODUCT
        product = Product.objects.create(
            shop=shop,
            product_status=status,
            **validated_data
        )

        product.categories.set(categories)

        # IMAGES
        if images:
            ProductImage.objects.bulk_create([
                ProductImage(product=product, **img)
                for img in images
            ])

        # OPTIONS
        if options:
            for opt in options:
                option = ProductOption.objects.create(
                    product=product,
                    name=opt["name"]
                )

                ProductOptionValue.objects.bulk_create([
                    ProductOptionValue(
                        option=option,
                        value=v if isinstance(v, str) else v["value"]
                    )
                    for v in opt.get("values", [])
                ])

        # VARIANTS
        if variants:
            ProductService.create_variants(product, variants)

        return product

    # =========================================================
    # UPDATE PRODUCT
    # =========================================================
    @staticmethod
    @transaction.atomic
    def update_product(instance, validated_data):

        if instance.product_status in [
            ProductStatus.DELETED,
            ProductStatus.ARCHIVED
        ]:
            raise ValidationError({"error": "Product cannot be updated"})

        images = validated_data.pop("images", None)
        options = validated_data.pop("options", None)
        variants = validated_data.pop("variants", None)
        category_ids = validated_data.pop("category_ids", None)

        # BASIC UPDATE
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # CATEGORIES
        if category_ids is not None:
            categories = ProductService.validate_categories(category_ids)
            instance.categories.set(categories)

        # IMAGES
        if images is not None:
            ProductService.validate_images(images)
            instance.images.all().delete()

            ProductImage.objects.bulk_create([
                ProductImage(product=instance, **img)
                for img in images
            ])

        # OPTIONS
        if options is not None:
            ProductService.validate_options(options)
            instance.options.all().delete()

            for opt in options:
                option = ProductOption.objects.create(
                    product=instance,
                    name=opt["name"]
                )

                ProductOptionValue.objects.bulk_create([
                    ProductOptionValue(
                        option=option,
                        value=v if isinstance(v, str) else v["value"]
                    )
                    for v in opt.get("values", [])
                ])

        # VARIANTS
        if variants is not None:
            ProductService.validate_variants(variants)
            instance.variants.all().delete()

            ProductService.create_variants(instance, variants)

            instance.product_status = ProductService.determine_product_status(
                instance.shop,
                variants
            )
            instance.save()

        return instance

    # =========================================================
    # SOFT DELETE
    # =========================================================
    @staticmethod
    def delete_product(instance):
        instance.product_status = ProductStatus.DELETED
        instance.save()

    # =========================================================
    # STATUS HELPERS
    # =========================================================
    @staticmethod
    def activate_product(instance):
        instance.product_status = ProductStatus.ACTIVE
        instance.save()

    @staticmethod
    def archive_product(instance):
        instance.product_status = ProductStatus.ARCHIVED
        instance.save()

    @staticmethod
    def mark_out_of_stock(instance):
        instance.product_status = ProductStatus.OUT_OF_STOCK
        instance.save()