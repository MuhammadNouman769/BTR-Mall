from rest_framework import serializers

from apps.products.models import (
    ProductOption,
    ProductOptionValue
)


class ProductOptionValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionValue
        fields = [
            "id",
            "value",
            "position"
        ]


class ProductOptionSerializer(serializers.ModelSerializer):

    values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = [
            "id",
            "product",
            "name",
            "position",
            "values"
        ]