from django.db.models import Prefetch

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)


class ProductOptionSelector:

    # =====================================================
    # BASE QUERYSET
    # =====================================================

    @staticmethod
    def base():

        values_qs = ProductOptionValue.objects.order_by(
            "position",
            "created_at",
        )

        return (
            ProductOption.objects
            .select_related(
                "product",
                "product__shop",
            )
            .prefetch_related(
                Prefetch(
                    "values",
                    queryset=values_qs,
                )
            )
            .order_by(
                "position",
                "-created_at",
            )
        )

    # =====================================================
    # LIST
    # =====================================================

    @classmethod
    def list(cls):

        return cls.base()

    # =====================================================
    # DETAIL
    # =====================================================

    @classmethod
    def detail(cls, pk):

        return cls.base().filter(
            pk=pk,
        )