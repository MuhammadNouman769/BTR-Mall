from rest_framework import serializers
from apps.products.models import ProductOption, ProductOptionValue


class ProductOptionValueSerializer(serializers.Serializer):
    value = serializers.CharField()
    position = serializers.IntegerField(required=False)


class ProductOptionCreateSerializer(serializers.ModelSerializer):
    values = ProductOptionValueSerializer(many=True)

    class Meta:
        model = ProductOption
        fields = ["product", "name", "position", "values"]