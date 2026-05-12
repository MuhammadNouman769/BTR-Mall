from rest_framework import serializers


class ProductImageRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()
    alt_text = serializers.CharField(required=False, allow_blank=True)
    position = serializers.IntegerField(required=False)


class ProductOptionValueRequestSerializer(serializers.Serializer):
    value = serializers.CharField()


class ProductOptionRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    values = ProductOptionValueRequestSerializer(many=True)


class ProductVariantRequestSerializer(serializers.Serializer):
    sku = serializers.CharField(required=False, allow_blank=True)
    barcode = serializers.CharField(required=False, allow_blank=True)

    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    stock_quantity = serializers.IntegerField(default=0)
    track_inventory = serializers.BooleanField(default=True)
    allow_backorder = serializers.BooleanField(default=False)

    option1 = serializers.CharField(required=False, allow_blank=True)
    option2 = serializers.CharField(required=False, allow_blank=True)
    option3 = serializers.CharField(required=False, allow_blank=True)


class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    short_description = serializers.CharField(required=False, allow_blank=True)
    description_html = serializers.CharField(required=False, allow_blank=True)

    brand = serializers.CharField(required=False, allow_blank=True)

    is_featured = serializers.BooleanField(default=False)
    is_best_seller = serializers.BooleanField(default=False)
    is_new = serializers.BooleanField(default=False)
    is_on_sale = serializers.BooleanField(default=False)

    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    images = ProductImageRequestSerializer(many=True, required=False)
    options = ProductOptionRequestSerializer(many=True, required=False)
    variants = ProductVariantRequestSerializer(many=True, required=False)