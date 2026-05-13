from rest_framework import serializers
from apps.products.models import Shop


class ShopTrashSerializer(serializers.ModelSerializer):

    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "handle",
            "owner_email",
            "shop_status",
            "is_verified",
            "created_at",
            "updated_at",
            "is_deleted",
        ]