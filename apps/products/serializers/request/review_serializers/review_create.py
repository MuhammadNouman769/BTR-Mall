from rest_framework import serializers

from apps.products.models.review import ProductReview


class ProductReviewCreateSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )

    class Meta:
        model = ProductReview

        fields = [
            "rating",
            "title",
            "comment",
            "images",
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5"
            )

        return value