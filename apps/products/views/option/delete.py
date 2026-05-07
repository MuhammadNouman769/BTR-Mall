from rest_framework import serializers

from apps.products.models import (
    ProductVariant,
    VariantImage
)


class VariantImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantImage
        fields = [
            "id",
            "image",
            "alt_text",
            "is_main",
            "position",
        ]


class ProductVariantCreateSerializer(serializers.ModelSerializer):

    variant_images = VariantImageSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = ProductVariant
        fields = [
            "id",
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

            "variant_images",
        ]

    def create(self, validated_data):
        images = validated_data.pop("variant_images", [])

        variant = ProductVariant.objects.create(**validated_data)

        for image in images:
            VariantImage.objects.create(
                variant=variant,
                **image
            )

        return variant

    def update(self, instance, validated_data):
        validated_data.pop("variant_images", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance