from rest_framework import serializers

from apps.products.models import VariantImage


# =========================================================
# VARIANT IMAGE
# =========================================================

class VariantImageResponseSerializer(serializers.ModelSerializer):

    class Meta:

        model = VariantImage

        fields = [
            "id",
            "variant",
            "image",
            "alt_text",
            "is_main",
            "position",
        ]


# =========================================================
# CREATE / UPDATE / DETAIL RESPONSE
# =========================================================

class VariantImageDetailResponseSerializer(serializers.Serializer):

    message = serializers.CharField()

    data = VariantImageResponseSerializer()


# =========================================================
# LIST RESPONSE
# =========================================================

class VariantImageListResponseSerializer(serializers.Serializer):

    message = serializers.CharField()

    data = VariantImageResponseSerializer(
        many=True,
    )


# =========================================================
# DELETE RESPONSE
# =========================================================

class VariantImageDeleteResponseSerializer(serializers.Serializer):

    message = serializers.CharField()