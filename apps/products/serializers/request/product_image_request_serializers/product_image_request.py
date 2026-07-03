from rest_framework import serializers

from apps.products.models import (
    Product,
    ProductImage,
)


class ProductImageCreateSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )

    image = serializers.ImageField()

    alt_text = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    position = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
    )

    class Meta:

        model = ProductImage

        fields = [
            "product",
            "image",
            "alt_text",
            "position",
        ]

    # =====================================================
    # IMAGE
    # =====================================================

    def validate_image(self, value):

        if not value:
            raise serializers.ValidationError(
                "Image is required."
            )

        return value

    # =====================================================
    # GLOBAL VALIDATION
    # =====================================================

    def validate(self, attrs):

        product = attrs.get("product")

        if not product:
            return attrs

        queryset = ProductImage.objects.filter(
            product=product,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.count() >= 10:
            raise serializers.ValidationError(
                {
                    "image": "Maximum 10 product images are allowed."
                }
            )

        return attrs