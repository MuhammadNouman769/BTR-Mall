from apps.products.models import VariantImage


class VariantImageSelector:

    # =====================================================
    # LIST
    # =====================================================

    @staticmethod
    def all():

        return (
            VariantImage.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .order_by(
                "position",
                "id",
            )
        )

    # =====================================================
    # DETAIL
    # =====================================================

    @staticmethod
    def detail(pk):

        return (
            VariantImage.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .filter(
                pk=pk,
            )
            .first()
        )

    # =====================================================
    # BY VARIANT
    # =====================================================

    @staticmethod
    def by_variant(variant_id):

        return (
            VariantImage.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .filter(
                variant_id=variant_id,
            )
            .order_by(
                "position",
                "id",
            )
        )

    # =====================================================
    # MAIN IMAGE
    # =====================================================

    @staticmethod
    def main_image(variant_id):

        return (
            VariantImage.objects
            .filter(
                variant_id=variant_id,
                is_main=True,
            )
            .first()
        )