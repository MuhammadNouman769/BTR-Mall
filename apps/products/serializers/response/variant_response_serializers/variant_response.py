from rest_framework import serializers

from apps.products.models import (
    ProductVariant,
    VariantImage,
)


# =========================================================
# VARIANT IMAGE RESPONSE
# =========================================================

class VariantImageResponseSerializer(serializers.ModelSerializer):

    class Meta:

        model = VariantImage

        fields = [
            "id",
            "image",
            "alt_text",
            "is_main",
            "position",
        ]


# =========================================================
# VARIANT RESPONSE
# =========================================================

class ProductVariantResponseSerializer(serializers.ModelSerializer):

    variant_name = serializers.CharField(
        source="get_variant_name",
        read_only=True,
    )

    is_in_stock = serializers.BooleanField(
        read_only=True,
    )

    class Meta:
        model = ProductVariant

        fields = [
            "id",
            "product",
            "sku",
            "barcode",
            "price",
            "compare_at_price",
            "stock_quantity",
            "track_inventory",
            "allow_backorder",
            "position",
            "variant_name",
            "is_in_stock",
        ]

# =========================================================
# CREATE / UPDATE RESPONSE
# =========================================================

class ProductVariantCreateUpdateResponseSerializer(serializers.Serializer):

    message = serializers.CharField()

    id = serializers.IntegerField()


# =========================================================
# DETAIL RESPONSE
# =========================================================

class ProductVariantDetailResponseSerializer(serializers.Serializer):

    message = serializers.CharField()

    data = ProductVariantResponseSerializer()


# =========================================================
# LIST RESPONSE
# =========================================================

class ProductVariantListResponseSerializer(serializers.Serializer):

    message = serializers.CharField()

    data = ProductVariantResponseSerializer(
        many=True,
    )


# =========================================================
# DELETE RESPONSE
# =========================================================

class ProductVariantDeleteResponseSerializer(serializers.Serializer):

    message = serializers.CharField()