# apps/products/serializers/request/product_resquest_serializers/product_request.py

from rest_framework import serializers

from apps.products.models import Product
from apps.products.models.category import Category
from apps.products.models.variant import ProductVariant


# =========================================================
# PRODUCT IMAGE
# =========================================================

class ProductImageRequestSerializer(serializers.Serializer):

    image = serializers.ImageField()

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

    image = serializers.ImageField()

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

    # =====================================================
    # SKU VALIDATION
    # =====================================================

    def validate_sku(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "SKU is too short"
            )

        if ProductVariant.objects.filter(
            sku=value
        ).exists():

            raise serializers.ValidationError(
                "SKU already exists"
            )

        return value

    # =====================================================
    # BARCODE VALIDATION
    # =====================================================

    def validate_barcode(self, value):

        if value:

            value = value.strip()

            if len(value) < 3:

                raise serializers.ValidationError(
                    "Barcode is too short"
                )

        return value

    # =====================================================
    # VARIANT VALIDATION
    # =====================================================

    def validate(self, attrs):

        option1 = attrs.get("option1")
        option2 = attrs.get("option2")
        option3 = attrs.get("option3")

        if not option1 and (option2 or option3):

            raise serializers.ValidationError(
                "Option1 is required if option2 or option3 is used"
            )

        price = attrs.get("price")

        if price <= 0:

            raise serializers.ValidationError(
                "Price must be greater than zero"
            )

        compare_at_price = attrs.get(
            "compare_at_price"
        )

        if (
            compare_at_price and
            compare_at_price <= price
        ):

            raise serializers.ValidationError(
                "Compare at price must be greater than price"
            )

        images = attrs.get("images", [])

        if len(images) > 5:

            raise serializers.ValidationError(
                "Maximum 5 variant images allowed"
            )

        return attrs


# =========================================================
# PRODUCT CREATE
# =========================================================

class ProductCreateSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
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
            "categories",

            # NESTED
            "images",
            "options",
            "variants",
        ]

    # =====================================================
    # TITLE VALIDATION
    # =====================================================

    def validate_title(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Product title is too short"
            )

        return value

    # =====================================================
    # CATEGORY VALIDATION
    # =====================================================

    def validate_categories(self, value):

        ids = [category.id for category in value]

        if len(ids) != len(set(ids)):

            raise serializers.ValidationError(
                "Duplicate categories are not allowed"
            )

        return value

    # =====================================================
    # VARIANTS VALIDATION
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
                "images":
                "Maximum 10 product images allowed"
            })

        return attrs