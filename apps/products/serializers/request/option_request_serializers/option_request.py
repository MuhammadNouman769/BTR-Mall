from rest_framework import serializers

from apps.products.models import (
    ProductOption,
)


# =========================================================
# OPTION VALUE
# =========================================================

class ProductOptionValueSerializer(serializers.Serializer):

    value = serializers.CharField()

    position = serializers.IntegerField(
        required=False,
    )


# =========================================================
# OPTION CREATE / UPDATE
# =========================================================

class ProductOptionCreateSerializer(serializers.ModelSerializer):

    values = ProductOptionValueSerializer(
        many=True,
    )

    class Meta:

        model = ProductOption

        fields = [
            "product",
            "name",
            "position",
            "values",
        ]

        # Disable DRF default UniqueTogetherValidator
        validators = []

    # =====================================================
    # NAME
    # =====================================================

    def validate_name(self, value):

        value = value.strip()

        if len(value) < 2:

            raise serializers.ValidationError(
                "Option name is too short."
            )

        return value

    # =====================================================
    # VALUES
    # =====================================================

    def validate_values(self, values):

        cleaned = set()

        for item in values:

            value = item["value"].strip()

            if not value:

                raise serializers.ValidationError(
                    "Option value cannot be empty."
                )

            lower_value = value.lower()

            if lower_value in cleaned:

                raise serializers.ValidationError(
                    "Duplicate option values are not allowed."
                )

            cleaned.add(lower_value)

            item["value"] = value

        return values

    # =====================================================
    # GLOBAL VALIDATION
    # =====================================================

    def validate(self, attrs):

        product = attrs["product"]

        name = attrs["name"].strip()

        queryset = ProductOption.objects.filter(
            product=product,
            name__iexact=name,
        )

        if self.instance:

            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():

            raise serializers.ValidationError(
                {
                    "name": (
                        "This option already exists "
                        "for this product."
                    )
                }
            )

        attrs["name"] = name

        return attrs