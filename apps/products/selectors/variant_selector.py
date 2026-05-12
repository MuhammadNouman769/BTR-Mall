from django.db.models import Prefetch

from apps.products.models import (
    ProductVariant,
    VariantImage,
)


class ProductVariantSelector:

    @staticmethod
    def list():

        variant_images_qs = VariantImage.objects.order_by(
            "position",
            "created_at"
        )

        return ProductVariant.objects.select_related(
            "product",
            "product__shop",
            "option1",
            "option2",
            "option3",
        ).prefetch_related(
            Prefetch(
                "variant_images",
                queryset=variant_images_qs
            )
        ).order_by(
            "position",
            "-created_at"
        )

    @staticmethod
    def detail(pk):

        variant_images_qs = VariantImage.objects.order_by(
            "position",
            "created_at"
        )

        return ProductVariant.objects.select_related(
            "product",
            "product__shop",
            "option1",
            "option2",
            "option3",
        ).prefetch_related(
            Prefetch(
                "variant_images",
                queryset=variant_images_qs
            )
        ).get(pk=pk)