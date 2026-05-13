from django.db.models import Prefetch

from apps.products.models import (
    Shop,
    Product
)


class ShopSelector:

    # =========================================================
    # BASE QUERYSET
    # =========================================================
    @staticmethod
    def base_queryset():

        return (
            Shop.objects
            .select_related("owner")
            .prefetch_related(
                Prefetch(
                    "products",
                    queryset=Product.objects.only(
                        "id",
                        "title",
                        "product_status"
                    )
                )
            )
        )

    # =========================================================
    # LIST SHOPS
    # =========================================================
    @classmethod
    def list_shops(cls):

        return cls.base_queryset()

    # =========================================================
    # DETAIL SHOP
    # =========================================================
    @classmethod
    def detail(cls, pk):

        return cls.base_queryset().get(pk=pk)

    # =========================================================
    # USER SHOP
    # =========================================================
    @classmethod
    def user_shop(cls, user):

        return cls.base_queryset().get(owner=user)