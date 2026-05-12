from rest_framework import serializers
from apps.products.models import ProductOption, ProductOptionValue


class ProductOptionValueSerializer(serializers.Serializer):
    value = serializers.CharField()
    position = serializers.IntegerField(required=False)


class ProductOptionCreateSerializer(serializers.ModelSerializer):

    values = ProductOptionValueSerializer(many=True)

    class Meta:
        model = ProductOption
        fields = [
            "product",
            "name",
            "position",
            "values"
        ]

    def validate_values(self, values):

        cleaned = [
            item["value"].strip().lower()
            for item in values
        ]

        if len(cleaned) != len(set(cleaned)):
            raise serializers.ValidationError(
                "Duplicate option values are not allowed"
            )

        return values