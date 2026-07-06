from rest_framework import serializers

from apps.products.models import (
    ProductVariant,
    VariantImage,
)


class VariantImageRequestSerializer(serializers.ModelSerializer):

    class Meta:

        model = VariantImage

        fields = [
            "variant",
            "image",
            "alt_text",
            "is_main",
            "position",
        ]

    # =====================================================
    # VARIANT
    # =====================================================

    def validate_variant(self, value):

        if not ProductVariant.objects.filter(
            pk=value.pk,
        ).exists():

            raise serializers.ValidationError(
                "Variant does not exist."
            )

        return value

    # =====================================================
    # IMAGE
    # =====================================================

    def validate_image(self, value):

        if value is None:

            raise serializers.ValidationError(
                "Image is required."
            )

        return value

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(self, attrs):

        variant = attrs.get(
            "variant",
            getattr(self.instance, "variant", None),
        )

        is_main = attrs.get(
            "is_main",
            False,
        )

        queryset = VariantImage.objects.filter(
            variant=variant,
            is_main=True,
        )

        if self.instance:

            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if is_main and queryset.exists():

            raise serializers.ValidationError(
                {
                    "is_main": (
                        "This variant already has a main image."
                    )
                }
            )

        return attrs