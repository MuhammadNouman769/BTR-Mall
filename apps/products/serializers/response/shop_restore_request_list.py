# serializers/response/shop_restore_request_list.py

from rest_framework import serializers
from apps.products.models.shop_restore_request import ShopActionRequest


class ShopRestoreRequestListSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source="shop.name")
    shop_id = serializers.IntegerField(source="shop.id")
    requested_by_email = serializers.EmailField(source="requested_by.email")

    class Meta:
        model = ShopActionRequest
        fields = [
            "id",
            "shop_id",
            "shop_name",
            "requested_by_email",
            "reason",
            "status",
            "created_at",
        ]