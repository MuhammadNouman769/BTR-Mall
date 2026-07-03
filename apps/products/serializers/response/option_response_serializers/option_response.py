from rest_framework import serializers
from apps.products.models import ProductOption, ProductOptionValue


class ProductOptionValueResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = ["id", "value", "position"]


class ProductOptionResponseSerializer(serializers.ModelSerializer):
    values = ProductOptionValueResponseSerializer(many=True, read_only=True)


    class Meta:
        model = ProductOption
        fields = ["id", "product", "name", "position", "values"]







class ProductOptionListResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ProductOptionResponseSerializer(many=True)