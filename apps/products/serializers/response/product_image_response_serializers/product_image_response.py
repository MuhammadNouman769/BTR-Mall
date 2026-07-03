from rest_framework import serializers

from apps.products.models import ProductImage


class ProductImageResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = [
            "id",
            "product",
            "image",
            "alt_text",
            "position",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class ProductImageListResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ProductImageResponseSerializer(many=True)