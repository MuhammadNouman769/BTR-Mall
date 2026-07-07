# apps/products/serializers/response/option_response_serializers/option_response.py

from rest_framework import serializers

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)


# =========================================================
# OPTION VALUE RESPONSE
# =========================================================

class ProductOptionValueResponseSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ProductOptionValue

        fields = [
            "id",
            "value",
            "position",
        ]


# =========================================================
# OPTION RESPONSE
# =========================================================

class ProductOptionResponseSerializer(
    serializers.ModelSerializer
):

    values = ProductOptionValueResponseSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = ProductOption

        fields = [
            "id",
            "product",
            "name",
            "position",
            "values",
        ]


# =========================================================
# DETAIL RESPONSE
# =========================================================

class ProductOptionDetailResponseSerializer(
    serializers.Serializer
):

    message = serializers.CharField()

    data = ProductOptionResponseSerializer()


# =========================================================
# LIST RESPONSE
# =========================================================

class ProductOptionListResponseSerializer(
    serializers.Serializer
):

    message = serializers.CharField()

    data = ProductOptionResponseSerializer(
        many=True,
    )