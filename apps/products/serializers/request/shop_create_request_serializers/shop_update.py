from rest_framework import serializers
from apps.products.models import Shop


class ShopUpdateSerializer(serializers.ModelSerializer):

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

    # =========================================================
    # FIELD VALIDATION
    # =========================================================
    def validate_cnic_number(self, value):

        if value:
            value = value.strip()

            if not value.isdigit():
                raise serializers.ValidationError(
                    "CNIC must contain only digits"
                )

            if len(value) != 13:
                raise serializers.ValidationError(
                    "CNIC must be exactly 13 digits"
                )

        return value