from rest_framework import serializers
from apps.products.models import ProductVariant, VariantImage


class VariantImageResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImage
        fields = ["id", "image", "alt_text", "is_main", "position"]


class ProductVariantResponseInProductSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="get_variant_name", read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    variant_images = VariantImageResponseSerializer(many=True, read_only=True)

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
            "variant_images",
        ]