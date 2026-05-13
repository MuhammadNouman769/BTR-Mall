# apps/products/selectors/product_selector.py

from django.db.models import Prefetch, Q, Min, Max
from django.shortcuts import get_object_or_404

from apps.products.models import (
    Product,
    ProductVariant,
)

from apps.common.enums import ProductStatus


class ProductSelector:

    # =========================================================
    # BOOLEAN PARSER
    # =========================================================
    @staticmethod
    def to_bool(value):

        return str(value).lower() in [
            "true",
            "1",
            "yes"
        ]

    # =========================================================
    # BASE QUERYSET (OPTIMIZED)
    # =========================================================
    @staticmethod
    def base_queryset():

        return (
            Product.objects
            .select_related("shop")
            .prefetch_related(
                "categories",
                "images",
                Prefetch(
                    "variants",
                    queryset=(
                        ProductVariant.objects
                        .select_related(
                            "option1",
                            "option2",
                            "option3",
                        )
                        .prefetch_related(
                            "variant_images"
                        )
                    )
                )
            )
            .annotate(
                min_price=Min("variants__price"),
                max_price=Max("variants__price"),
            )
        )

    # =========================================================
    # ROLE BASED QUERYSET
    # =========================================================
    @classmethod
    def get_role_based_queryset(cls, user):

        if user and user.is_staff:
            return cls.admin_products()

        elif user and hasattr(user, "shop"):
            return cls.seller_products(user)

        return cls.public_products()

    # =========================================================
    # PUBLIC PRODUCTS
    # =========================================================
    @classmethod
    def public_products(cls):

        return cls.base_queryset().filter(
            product_status=ProductStatus.ACTIVE
        )

    # =========================================================
    # SELLER PRODUCTS
    # =========================================================
    @classmethod
    def seller_products(cls, user):

        return cls.base_queryset().filter(
            shop=user.shop
        )

    # =========================================================
    # ADMIN PRODUCTS
    # =========================================================
    @classmethod
    def admin_products(cls):

        return cls.base_queryset()

    # =========================================================
    # LIST PRODUCTS
    # =========================================================
    @classmethod
    def list_products(cls, filters=None, user=None):

        qs = cls.get_role_based_queryset(user)

        qs = cls.apply_filters(
            qs,
            filters
        )

        return qs.distinct()

    # =========================================================
    # PRODUCT DETAIL
    # =========================================================
    @classmethod
    def detail(cls, pk, user=None):

        qs = cls.get_role_based_queryset(user)

        return get_object_or_404(
            qs,
            pk=pk
        )

    # =========================================================
    # FILTER ENGINE
    # =========================================================
    @staticmethod
    def apply_filters(qs, filters):

        if not filters:
            return qs

        # =====================================================
        # NORMALIZER
        # =====================================================
        def get(name):

            value = filters.get(name)

            if value in [None, "", "null"]:
                return None

            return value

        # =====================================================
        # CATEGORY
        # =====================================================
        category = get("category")

        if category:

            qs = qs.filter(
                categories__id=category
            )

        # =====================================================
        # SHOP
        # =====================================================
        shop = get("shop")

        if shop:

            qs = qs.filter(
                shop_id=shop
            )

        # =====================================================
        # STATUS
        # =====================================================
        status = get("status")

        if status:

            qs = qs.filter(
                product_status=status
            )

        # =====================================================
        # SEARCH
        # =====================================================
        search = get("search")

        if search:

            qs = qs.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description_html__icontains=search) |
                Q(brand__icontains=search)
            )

        # =====================================================
        # FEATURED
        # =====================================================
        featured = get("featured")

        if featured is not None:

            qs = qs.filter(
                is_featured=ProductSelector.to_bool(
                    featured
                )
            )

        # =====================================================
        # BEST SELLER
        # =====================================================
        best_seller = get("best_seller")

        if best_seller is not None:

            qs = qs.filter(
                is_best_seller=ProductSelector.to_bool(
                    best_seller
                )
            )

        # =====================================================
        # ON SALE
        # =====================================================
        on_sale = get("on_sale")

        if on_sale is not None:

            qs = qs.filter(
                is_on_sale=ProductSelector.to_bool(
                    on_sale
                )
            )

        # =====================================================
        # BRAND
        # =====================================================
        brand = get("brand")

        if brand:

            qs = qs.filter(
                brand__iexact=brand
            )

        # =====================================================
        # PRICE RANGE
        # =====================================================
        min_price = get("min_price")
        max_price = get("max_price")

        if min_price:

            qs = qs.filter(
                variants__price__gte=min_price
            )

        if max_price:

            qs = qs.filter(
                variants__price__lte=max_price
            )

        # =====================================================
        # STOCK
        # =====================================================
        in_stock = get("in_stock")

        if in_stock:

            qs = qs.filter(
                variants__stock_quantity__gt=0
            )

        # =====================================================
        # SORTING
        # =====================================================
        ordering = get("ordering")

        allowed_ordering = {
            "created_at",
            "-created_at",
            "title",
            "-title",
            "average_rating",
            "-average_rating",
            "total_sold",
            "-total_sold",
            "min_price",
            "-min_price",
            "max_price",
            "-max_price",
        }

        if ordering in allowed_ordering:

            qs = qs.order_by(ordering)

        else:

            qs = qs.order_by("-created_at")

        return qs