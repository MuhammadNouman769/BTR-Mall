from rest_framework import serializers

from apps.products.models import ProductVariant


class ProductVariantCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductVariant

        fields = [


            "sku",
            "barcode",

            "option1",
            "option2",
            "option3",

            "price",
            "compare_at_price",

            "stock_quantity",

            "track_inventory",
            "allow_backorder",

            "position",
        ]

    # =====================================================
    # SKU
    # =====================================================

    def validate_sku(self, value):

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "SKU is too short."
            )

        queryset = ProductVariant.objects.filter(
            sku=value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "SKU already exists."
            )

        return value

    # =====================================================
    # BARCODE
    # =====================================================

    def validate_barcode(self, value):

        if not value:
            return value

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Barcode is too short."
            )

        return value

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(self, attrs):

        option1 = attrs.get("option1")
        option2 = attrs.get("option2")
        option3 = attrs.get("option3")

        if not option1 and (option2 or option3):

            raise serializers.ValidationError(
                "Option1 is required if Option2 or Option3 is provided."
            )

        price = attrs["price"]

        if price <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        compare_price = attrs.get(
            "compare_at_price"
        )

        if (
            compare_price is not None
            and compare_price <= price
        ):
            raise serializers.ValidationError(
                "Compare at price must be greater than price."
            )

        return attrs