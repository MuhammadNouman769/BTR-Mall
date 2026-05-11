from apps.products.models.review import ProductReview


class ProductReviewSelector:

    @staticmethod
    def get_product_reviews(product_id):

        return ProductReview.objects.filter(
            product_id=product_id,
            is_approved=True,
            is_deleted=False
        ).select_related(
            "user",
            "product"
        ).prefetch_related(
            "images"
        )

    @staticmethod
    def get_review_by_id(review_id):

        return ProductReview.objects.select_related(
            "user",
            "product"
        ).prefetch_related(
            "images"
        ).get(id=review_id)