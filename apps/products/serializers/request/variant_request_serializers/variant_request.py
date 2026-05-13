from rest_framework import serializers
from apps.products.models import ProductVariant, VariantImage


class VariantImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    alt_text = serializers.CharField(required=False, allow_blank=True)
    is_main = serializers.BooleanField(default=False)


class ProductVariantCreateSerializer(serializers.ModelSerializer):
    images = VariantImageSerializer(many=True, required=False)

    class Meta:
        model = ProductVariant
        fields = [
            "product",
            "sku",
            "barcode",
            "option1",
            "option2",
            "option3",
            "price",
            "compare_at_price",
            "stock_quantity",
            "track_inventory",
            "allow_backorder",
            "position",
            "images",
        ]