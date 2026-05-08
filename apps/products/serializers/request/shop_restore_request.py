from rest_framework import serializers


class ShopRestoreRequestSerializer(serializers.Serializer):
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500
    )