from rest_framework import serializers

from apps.products.models import (
    ProductReview,
    ProductReviewImage
)
from drf_spectacular.utils import extend_schema_field

class ProductReviewImageResponseSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductReviewImage

        fields = [
            "id",
            "image",
            "alt_text"
        ]
    @extend_schema_field(str)
    def get_image(self, obj):

        request = self.context.get("request")

        if obj.image:
            if request:
                return request.build_absolute_uri(
                    obj.image.url
                )

            return obj.image.url

        return None


class ProductReviewResponseSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True
    )

    user_name = serializers.CharField(
        source="user.full_name",
        read_only=True
    )

    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    images = ProductReviewImageResponseSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductReview

        fields = [
            "id",

            "product_id",
            "product_title",

            "user_id",
            "user_name",

            "rating",
            "title",
            "comment",

            "is_verified_purchase",
            "is_approved",

            "helpful_count",

            "images",

            "created_at",
            "updated_at",
        ]