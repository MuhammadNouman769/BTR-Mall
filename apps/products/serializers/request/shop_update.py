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

    def update(self, instance, validated_data):
        # simple clean update (partial supported)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance