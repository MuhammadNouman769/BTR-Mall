from rest_framework import serializers


class ShopHardDeleteResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    id = serializers.IntegerField()