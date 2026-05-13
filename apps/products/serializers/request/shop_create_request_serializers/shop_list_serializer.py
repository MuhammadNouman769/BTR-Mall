from rest_framework import serializers

from apps.products.models import Shop


class ShopListSerializer(serializers.ModelSerializer):

    owner_email = serializers.EmailField(
        source="owner.email",
        read_only=True
    )

    class Meta:

        model = Shop

        fields = [
            "id",
            "name",
            "handle",
            "owner_email",
            "shop_status",
            "is_verified",
            "rating",
            "created_at",
        ]