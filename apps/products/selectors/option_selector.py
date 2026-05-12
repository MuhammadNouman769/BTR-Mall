from django.db.models import Prefetch

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)


class ProductOptionSelector:

    @staticmethod
    def base():

        values_qs = ProductOptionValue.objects.order_by(
            "position",
            "created_at"
        )

        return ProductOption.objects.select_related(
            "product",
            "product__shop",
        ).prefetch_related(
            Prefetch(
                "values",
                queryset=values_qs
            )
        ).order_by(
            "position",
            "-created_at"
        )

    @classmethod
    def list(cls):
        return cls.base()

    @classmethod
    def detail(cls, pk):
        return cls.base().get(pk=pk)