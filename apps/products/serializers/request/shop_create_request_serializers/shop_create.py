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

    def validate_cnic_number(self, value):

        value = value.strip()

        if len(value) != 13:
            raise serializers.ValidationError(
                "CNIC must contain 13 digits"
            )

        if not value.isdigit():
            raise serializers.ValidationError(
                "CNIC must contain only digits"
            )

        return value
    

    