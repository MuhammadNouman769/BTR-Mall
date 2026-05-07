from apps.products.models import ProductOption


class ProductOptionSelector:

    @staticmethod
    def base():
        return ProductOption.objects.select_related(
            "product"
        ).prefetch_related(
            "values"
        )

    @classmethod
    def list(cls):
        return cls.base()

    @classmethod
    def detail(cls, pk):
        return cls.base().get(pk=pk)