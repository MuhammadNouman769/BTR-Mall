from rest_framework import serializers

from apps.products.models import (
    Product,
    Category,
)

# =========================================================
# PRODUCT IMAGE
# =========================================================

class ProductImageRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()
    alt_text = serializers.CharField(required=False, allow_blank=True)
    position = serializers.IntegerField(required=False, default=0)


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
    values = ProductOptionValueRequestSerializer(many=True)


# =========================================================
# VARIANT IMAGE
# =========================================================

class VariantImageRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()
    alt_text = serializers.CharField(required=False, allow_blank=True)
    is_main = serializers.BooleanField(default=False)
    position = serializers.IntegerField(default=0)


# =========================================================
# VARIANT
# =========================================================

class ProductVariantRequestSerializer(serializers.Serializer):

    sku = serializers.CharField()
    barcode = serializers.CharField(required=False, allow_blank=True)

    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    compare_at_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )

    stock_quantity = serializers.IntegerField(default=0)

    track_inventory = serializers.BooleanField(default=True)

    allow_backorder = serializers.BooleanField(default=False)

    option1 = serializers.IntegerField(required=False)
    option2 = serializers.IntegerField(required=False)
    option3 = serializers.IntegerField(required=False)

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
            "title",
            "short_description",
            "description_html",

            "brand",

            "meta_title",
            "meta_description",
            "meta_keywords",

            "is_featured",
            "is_best_seller",
            "is_new",
            "is_on_sale",

            "category_ids",

            "images",
            "options",
            "variants",
        ]