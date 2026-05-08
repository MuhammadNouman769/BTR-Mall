from rest_framework import serializers


class ShopRestoreResponseSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    shop_id = serializers.IntegerField(read_only=True)
    shop_name = serializers.CharField(read_only=True)

    reason = serializers.CharField(read_only=True)

    status = serializers.CharField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)

    reviewed_at = serializers.DateTimeField(read_only=True)

    reviewed_by = serializers.CharField(read_only=True)