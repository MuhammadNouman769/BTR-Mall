from django.db import transaction

from apps.products.models import ProductImage


class ProductImageService:

    @staticmethod
    @transaction.atomic
    def create_images(product, images):

        if not images:
            return

        ProductImage.objects.bulk_create([
            ProductImage(
                product=product,
                image=img["image"],
                alt_text=img.get("alt_text", ""),
                position=img.get("position", 0),
            )
            for img in images
        ])

    @staticmethod
    @transaction.atomic
    def update_images(product, images):

        if images is None:
            return

        product.images.all().delete()

        ProductImageService.create_images(
            product,
            images
        )