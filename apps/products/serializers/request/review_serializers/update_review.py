from rest_framework import serializers

from apps.products.models.review import ProductReview


class ProductReviewUpdateSerializer(serializers.ModelSerializer):

    new_images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )

    deleted_images = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = ProductReview

        fields = [
            "rating",
            "title",
            "comment",
            "new_images",
            "deleted_images",
        ]