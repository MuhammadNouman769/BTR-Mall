from django.db.models import Prefetch, Q, Min, Max

from apps.products.models import (
    Product,
    ProductVariant,
)

from apps.common.enums import ProductStatus


class ProductSelector:

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
                    queryset=ProductVariant.objects
                    .select_related(
                        "option1",
                        "option2",
                        "option3"
                    )
                    .prefetch_related("variant_images")
                )
            )
        )

    # =========================================================
    # ROLE BASED QUERIES
    # =========================================================
    @classmethod
    def public_products(cls):
        return cls.base_queryset().filter(
            product_status=ProductStatus.ACTIVE
        )

    @classmethod
    def seller_products(cls, user):
        return cls.base_queryset().filter(
            shop=user.shop
        )

    @classmethod
    def admin_products(cls):
        return cls.base_queryset()

    # =========================================================
    # SMART ENTRY POINT
    # =========================================================
    @classmethod
    def list_products(cls, filters=None, user=None):

        if user and user.is_staff:
            qs = cls.admin_products()

        elif user and hasattr(user, "shop"):
            qs = cls.seller_products(user)

        else:
            qs = cls.public_products()

        return cls.apply_filters(qs, filters).distinct()

    # =========================================================
    # DETAIL
    # =========================================================
    @classmethod
    def detail(cls, pk, user=None):

        if user and user.is_staff:
            qs = cls.admin_products()

        elif user and hasattr(user, "shop"):
            qs = cls.seller_products(user)

        else:
            qs = cls.public_products()

        return qs.get(pk=pk)

    # =========================================================
    # FILTER ENGINE (IMPROVED)
    # =========================================================
    @staticmethod
    def apply_filters(qs, filters):

        if not filters:
            return qs

        # Normalize filters (important for query_params)
        def get(name):
            val = filters.get(name)
            return val if val not in [None, "", "null"] else None

        # ---------------- CATEGORY ----------------
        category = get("category")
        if category:
            qs = qs.filter(categories__id=category)

        # ---------------- SHOP ----------------
        shop = get("shop")
        if shop:
            qs = qs.filter(shop_id=shop)

        # ---------------- STATUS ----------------
        status = get("status")
        if status:
            qs = qs.filter(product_status=status)

        # ---------------- SEARCH ----------------
        search = get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description_html__icontains=search) |
                Q(brand__icontains=search)
            )

        # ---------------- FLAGS ----------------
        if filters.get("featured") is not None:
            qs = qs.filter(is_featured=filters.get("featured") == "true")

        if filters.get("best_seller") is not None:
            qs = qs.filter(is_best_seller=filters.get("best_seller") == "true")

        if filters.get("on_sale") is not None:
            qs = qs.filter(is_on_sale=filters.get("on_sale") == "true")

        # ---------------- BRAND ----------------
        brand = get("brand")
        if brand:
            qs = qs.filter(brand__iexact=brand)

        # ---------------- PRICE RANGE ----------------
        min_price = get("min_price")
        max_price = get("max_price")

        if min_price:
            qs = qs.filter(variants__price__gte=min_price)

        if max_price:
            qs = qs.filter(variants__price__lte=max_price)

        # ---------------- STOCK ----------------
        if get("in_stock"):
            qs = qs.filter(variants__stock_quantity__gt=0)

        # =========================================================
        # SORTING (SAFE)
        # =========================================================
        ordering = get("ordering")

        allowed = {
            "created_at",
            "-created_at",
            "title",
            "-title",
            "average_rating",
            "-average_rating",
            "total_sold",
            "-total_sold",
        }

        qs = qs.order_by(ordering if ordering in allowed else "-created_at")

        return qs