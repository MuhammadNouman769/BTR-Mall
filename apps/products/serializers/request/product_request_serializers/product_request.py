# apps/products/serializers/request/product_request_serializers/product_request.py

from rest_framework import serializers
from apps.products.serializers.request.variant_request_serializers.variant_request import (
    ProductVariantCreateSerializer
)
from apps.products.models import (
    Product,
    Category,
    ProductVariant,
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
# PRODUCT CREATE
# =========================================================

class ProductCreateSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False,
    )

    options = ProductOptionRequestSerializer(
        many=True,
        required=False,
    )

    variants = ProductVariantCreateSerializer(
        many=True,
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
            "options",
            "variants",
        ]

    # =====================================================
    # TITLE
    # =====================================================

    def validate_title(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Product title is too short"
            )

        return value

    # =====================================================
    # CATEGORY
    # =====================================================

    def validate_categories(self, value):

        ids = [category.id for category in value]

        if len(ids) != len(set(ids)):

            raise serializers.ValidationError(
                "Duplicate categories are not allowed"
            )

        return value

    # =====================================================
    # VARIANTS
    # =====================================================

    def validate_variants(self, value):

        if not value:

            raise serializers.ValidationError(
                "At least one variant is required"
            )

        return value