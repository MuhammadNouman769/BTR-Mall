from rest_framework import serializers
from apps.products.models import Shop


class ShopCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop

        fields = [
            "name",
            "description",

            "logo",
            "banner",

            "cnic_number",
            "cnic_front",
            "cnic_back",
        ]

        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
            "cnic_number": {"required": True},

            # optional media fields
            "logo": {"required": False},
            "banner": {"required": False},
            "cnic_front": {"required": False},
            "cnic_back": {"required": False},
        }

    def validate_cnic_number(self, value):

        value = value.strip()

        if len(value) != 13 or not value.isdigit():
            raise serializers.ValidationError(
                "CNIC number must contain exactly 13 digits"
            )

        return value