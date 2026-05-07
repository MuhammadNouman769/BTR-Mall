from apps.products.models import ProductVariant


class ProductVariantSelector:

    @staticmethod
    def list():
        return ProductVariant.objects.select_related(
            "product",
            "option1",
            "option2",
            "option3",
        ).prefetch_related(
            "variant_images"
        )

    @staticmethod
    def detail(pk):
        return ProductVariant.objects.select_related(
            "product",
            "option1",
            "option2",
            "option3",
        ).prefetch_related(
            "variant_images"
        ).get(pk=pk)