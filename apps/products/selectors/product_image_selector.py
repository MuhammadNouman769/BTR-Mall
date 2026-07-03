from django.shortcuts import get_object_or_404

from apps.products.models import ProductImage


class ProductImageSelector:

    # =====================================================
    # LIST
    # =====================================================

    @staticmethod
    def list(filters=None):

        queryset = ProductImage.objects.select_related(
            "product",
        ).order_by(
            "position",
            "id",
        )

        if not filters:
            return queryset

        product = filters.get("product")

        if product:
            queryset = queryset.filter(
                product_id=product,
            )

        return queryset

    # =====================================================
    # DETAIL
    # =====================================================

    @staticmethod
    def detail(pk):

        return get_object_or_404(
            ProductImage.objects.select_related(
                "product",
            ),
            pk=pk,
        )