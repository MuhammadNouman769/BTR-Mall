from rest_framework import serializers

from apps.products.models import (
    Product,
    ProductImage,
    ProductVariant,
    ProductOption,
    ProductOptionValue,
    VariantImage,
)
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_field



# =========================================================
# PRODUCT IMAGE
# =========================================================

class ProductImageResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = [
            "id",
            "image",
            "alt_text",
            "position",
        ]


# =========================================================
# VARIANT IMAGE
# =========================================================

class VariantImageInProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantImage

        fields = ["id", "image", "alt_text", "is_main", "position",]
        ref_name = "VariantImageInProductSerializer"


# =========================================================
# OPTION VALUE
# =========================================================

class ProductOptionValueInProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionValue

        fields = ["id", "value", "position"]
        ref_name = "ProductOptionValueInProductSerializer"


# =========================================================
# OPTION
# =========================================================

class ProductOptionInProductSerializer(serializers.ModelSerializer):

    values = ProductOptionValueInProductSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductOption

        fields = [ "id", "name", "position", "values",]
        ref_name = "ProductOptionInProductSerializer"


# =========================================================
# VARIANT
# =========================================================

class ProductVariantResponseSerializer(serializers.ModelSerializer):

    variant_images = VariantImageInProductSerializer(
        many=True,
        read_only=True
    )

    variant_name = serializers.CharField(
        source="get_variant_name",
        read_only=True
    )

    class Meta:
        model = ProductVariant

        fields = [
            "id",

            "sku",
            "barcode",

            "price",
            "compare_at_price",

            "stock_quantity",

            "track_inventory",
            "allow_backorder",

            "variant_name",

            "variant_images",
        ]


# =========================================================
# PRODUCT LIST
# =========================================================

class ProductListResponseSerializer(serializers.ModelSerializer):

    main_image = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = [
            "id",
            "title",
            "handle",
            "brand",

            "product_status",

            "main_image",

            "price",

            "average_rating",

            "total_reviews",
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_main_image(self, obj):
        image = obj.images.first()
        if image:
            return image.image.url
        return None


    @extend_schema_field(serializers.FloatField())
    def get_price(self, obj):
        variant = obj.variants.first()
        if variant:
            return variant.price
        return 0


# =========================================================
# PRODUCT DETAIL
# =========================================================

class ProductDetailResponseSerializer(serializers.ModelSerializer):

    images = ProductImageResponseSerializer(
        many=True,
        read_only=True
    )

    options = ProductOptionInProductSerializer(
        many=True,
        read_only=True
    )

    variants = ProductVariantResponseSerializer(
        many=True,
        read_only=True
    )

    categories = serializers.StringRelatedField(
        many=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "title",
            "handle",
            "brand",
            "product_status",
            "description_html",
            "short_description",
            "images",
            "options",
            "variants",
            "categories",
        ] 
        
        


class PaginatedProductResponseSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    results = ProductListResponseSerializer(many=True)
        