from apps.products.models import Category


class CategorySelector:

    # =====================================================
    # BASE QUERYSET
    # =====================================================

    @staticmethod
    def base_queryset():

        return (
            Category.objects
            .select_related("parent")
            .prefetch_related("children")
        )

    # =====================================================
    # LIST
    # =====================================================

    @classmethod
    def list(cls):

        return cls.base_queryset().order_by(
            "position",
            "name",
        )

    # =====================================================
    # DETAIL
    # =====================================================

    @classmethod
    def detail(cls, pk):

        return cls.base_queryset().filter(
            pk=pk
        ).first()