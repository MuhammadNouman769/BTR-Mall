from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.products.models.review import (
    ProductReview,
    ProductReviewImage
)


class ProductReviewService:

    @staticmethod
    @transaction.atomic
    def create_review(user, product, validated_data):

        images = validated_data.pop("images", [])

        existing = ProductReview.objects.filter(
            user=user,
            product=product
        ).exists()

        if existing:
            raise ValidationError({
                "error": "You already reviewed this product"
            })

        review = ProductReview.objects.create(
            user=user,
            product=product,
            **validated_data
        )

        image_objects = []

        for image in images:
            image_objects.append(
                ProductReviewImage(
                    review=review,
                    image=image
                )
            )

        ProductReviewImage.objects.bulk_create(
            image_objects
        )

        return review




    @staticmethod
    @transaction.atomic
    def update_review(review, validated_data):

        new_images = validated_data.pop(
            "new_images",
            []
        )

        deleted_images = validated_data.pop(
            "deleted_images",
            []
        )

        for attr, value in validated_data.items():
            setattr(review, attr, value)

        review.save()

        if deleted_images:
            ProductReviewImage.objects.filter(
                id__in=deleted_images,
                review=review
            ).delete()

        new_image_objects = []

        for image in new_images:
            new_image_objects.append(
                ProductReviewImage(
                    review=review,
                    image=image
                )
            )

        ProductReviewImage.objects.bulk_create(
            new_image_objects
        )

        return review