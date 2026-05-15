# apps/products/serializers/request/product_resquest_serializers/product_request.py

from rest_framework import serializers

from apps.products.models import Product


# =========================================================
# PRODUCT IMAGE
# =========================================================

class ProductImageRequestSerializer(serializers.Serializer):

    image = serializers.FileField()

    alt_text = serializers.CharField(
        required=False,
        allow_blank=True
    )

    position = serializers.IntegerField(
        required=False,
        default=0
    )


# =========================================================
# OPTION VALUE
# =========================================================

class ProductOptionValueRequestSerializer(serializers.Serializer):

    value = serializers.CharField()


# =========================================================
# OPTION
# =========================================================

class ProductOptionRequestSerializer(serializers.Serializer):

    name = serializers.CharField()

    values = ProductOptionValueRequestSerializer(
        many=True
    )


# =========================================================
# VARIANT IMAGE
# =========================================================

class VariantImageRequestSerializer(serializers.Serializer):

    image = serializers.FileField()

    alt_text = serializers.CharField(
        required=False,
        allow_blank=True
    )

    is_main = serializers.BooleanField(
        default=False
    )

    position = serializers.IntegerField(
        default=0
    )


# =========================================================
# VARIANT
# =========================================================

class ProductVariantRequestSerializer(serializers.Serializer):

    sku = serializers.CharField()

    barcode = serializers.CharField(
        required=False,
        allow_blank=True
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    compare_at_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )

    stock_quantity = serializers.IntegerField(
        default=0
    )

    track_inventory = serializers.BooleanField(
        default=True
    )

    allow_backorder = serializers.BooleanField(
        default=False
    )

    option1 = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    option2 = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    option3 = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    images = VariantImageRequestSerializer(
        many=True,
        required=False
    )


# =========================================================
# PRODUCT CREATE
# =========================================================

class ProductCreateSerializer(serializers.ModelSerializer):

    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )

    images = ProductImageRequestSerializer(
        many=True,
        required=False
    )

    options = ProductOptionRequestSerializer(
        many=True,
        required=False
    )

    variants = ProductVariantRequestSerializer(
        many=True
    )

    class Meta:

        model = Product

        fields = [

            # BASIC
            "title",
            "short_description",
            "description_html",

            # BRAND
            "brand",

            # SEO
            "meta_title",
            "meta_description",
            "meta_keywords",

            # FLAGS
            "is_featured",
            "is_best_seller",
            "is_new",
            "is_on_sale",

            # RELATIONS
            "category_ids",

            # NESTED
            "images",
            "options",
            "variants",
        ]

    # =====================================================
    # VALIDATE TITLE
    # =====================================================

    def validate_title(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Product title is too short"
            )

        return value.strip()

    # =====================================================
    # VALIDATE CATEGORY IDS
    # =====================================================

    def validate_category_ids(self, value):

        if len(set(value)) != len(value):

            raise serializers.ValidationError(
                "Duplicate category ids are not allowed"
            )

        return value

    # =====================================================
    # VALIDATE VARIANTS
    # =====================================================

    def validate_variants(self, value):

        if not value:

            raise serializers.ValidationError(
                "At least one variant is required"
            )

        return value

    # =====================================================
    # GLOBAL VALIDATION
    # =====================================================

    def validate(self, attrs):

        images = attrs.get("images", [])

        if len(images) > 10:

            raise serializers.ValidationError({
                "images": "Maximum 10 product images allowed"
            })

        return attrs