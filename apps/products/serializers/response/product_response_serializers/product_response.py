from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.products.models import (
    Product,
    ProductImage,
    ProductVariant,
    ProductOption,
    ProductOptionValue,
    VariantImage,
    Category,
)
from apps.products.serializers.response.option_response_serializers.option_response import (
        ProductOptionResponseSerializer,
)
from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
ProductImageResponseSerializer,
)
from apps.products.serializers.response.variant_response_serializers.variant_response import (
ProductVariantResponseSerializer,
)
from apps.products.serializers.response.categories_response_serializers.category_response import (
CategorySerializer
)

# =========================================================
# PRODUCT LIST
# =========================================================

class ProductListResponseSerializer(
    serializers.ModelSerializer
):

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

    @extend_schema_field(
        serializers.CharField(
            allow_null=True
        )
    )
    def get_main_image(self, obj):

        image = (
            obj.images
            .order_by("position")
            .first()
        )

        if image:
            return image.image.url

        return None

    @extend_schema_field(
        serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
            allow_null=True,
        )
    )
    def get_price(self, obj):

        variant = (
            obj.variants
            .order_by("position")
            .first()
        )

        if variant:
            return variant.price

        return None


# =========================================================
# PRODUCT DETAIL
# =========================================================

class ProductDetailResponseSerializer(
    serializers.ModelSerializer
):

    images = ProductImageResponseSerializer(
        many=True,
        read_only=True,
    )

    options = ProductOptionResponseSerializer(
        many=True,
        read_only=True,
    )

    variants = ProductVariantResponseSerializer(
        many=True,
        read_only=True,
    )

    categories = ProductVariantResponseSerializer(
        many=True,
        read_only=True,
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

            "average_rating",

            "total_reviews",
        ]


class PaginatedProductResponseSerializer(serializers.Serializer):

    count = serializers.IntegerField()

    next = serializers.CharField(
        allow_null=True,
    )

    previous = serializers.CharField(
        allow_null=True,
    )

    results = ProductListResponseSerializer(
        many=True,
    )