from rest_framework import serializers

from apps.products.models import Shop


class ShopDetailSerializer(serializers.ModelSerializer):

    owner_email = serializers.EmailField(
        source="owner.email",
        read_only=True
    )

    class Meta:

        model = Shop

        exclude = [
            "owner"
        ]