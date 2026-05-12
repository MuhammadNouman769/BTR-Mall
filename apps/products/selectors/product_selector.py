from django.db.models import Prefetch, Q

from apps.products.models import (
    Product,
    ProductImage,
    ProductVariant,
)

from apps.common.enums import ProductStatus


class ProductSelector:

    # =========================================================
    # BASE QUERYSET
    # =========================================================
    @staticmethod
    def base_queryset():

        return Product.objects.select_related(
            "shop",
        ).prefetch_related(
            "categories",
            "images",
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.prefetch_related(
                    "variant_images"
                )
            )
        )

    # =========================================================
    # PUBLIC PRODUCTS
    # Only visible/live products
    # =========================================================
    @classmethod
    def public_products(cls):

        return cls.base_queryset().filter(
            product_status=ProductStatus.ACTIVE
        )

    # =========================================================
    # SELLER PRODUCTS
    # Seller can see all own products
    # =========================================================
    @classmethod
    def seller_products(cls, seller):

        return cls.base_queryset().filter(
            shop=seller.shop
        )

    # =========================================================
    # ADMIN PRODUCTS
    # Admin sees everything
    # =========================================================
    @classmethod
    def admin_products(cls):

        return cls.base_queryset()

    # =========================================================
    # LIST PRODUCTS
    # =========================================================
    @classmethod
    def list_products(cls, filters=None, user=None):

        # -----------------------------------------
        # Role based queryset
        # -----------------------------------------
        if user and user.is_staff:
            qs = cls.admin_products()

        elif user and hasattr(user, "shop"):
            qs = cls.seller_products(user)

        else:
            qs = cls.public_products()

        # -----------------------------------------
        # Apply filters
        # -----------------------------------------
        qs = cls.apply_filters(qs, filters)

        return qs.distinct()

    # =========================================================
    # PRODUCT DETAIL
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
    # FILTER SYSTEM
    # =========================================================
    @staticmethod
    def apply_filters(qs, filters):

        if not filters:
            return qs

        # -----------------------------------------------------
        # CATEGORY FILTER
        # -----------------------------------------------------
        category = filters.get("category")

        if category:
            qs = qs.filter(
                categories__id=category
            )

        # -----------------------------------------------------
        # SHOP FILTER
        # -----------------------------------------------------
        shop = filters.get("shop")

        if shop:
            qs = qs.filter(
                shop_id=shop
            )

        # -----------------------------------------------------
        # STATUS FILTER
        # Admin/Seller use
        # -----------------------------------------------------
        status = filters.get("status")

        if status:
            qs = qs.filter(
                product_status=status
            )

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------
        search = filters.get("search")

        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description_html__icontains=search) |
                Q(brand__icontains=search)
            )

        # -----------------------------------------------------
        # FEATURED
        # -----------------------------------------------------
        featured = filters.get("featured")

        if featured is not None:
            qs = qs.filter(
                is_featured=featured
            )

        # -----------------------------------------------------
        # BEST SELLER
        # -----------------------------------------------------
        best_seller = filters.get("best_seller")

        if best_seller is not None:
            qs = qs.filter(
                is_best_seller=best_seller
            )

        # -----------------------------------------------------
        # ON SALE
        # -----------------------------------------------------
        on_sale = filters.get("on_sale")

        if on_sale is not None:
            qs = qs.filter(
                is_on_sale=on_sale
            )

        # -----------------------------------------------------
        # BRAND
        # -----------------------------------------------------
        brand = filters.get("brand")

        if brand:
            qs = qs.filter(
                brand__iexact=brand
            )

        # -----------------------------------------------------
        # PRICE RANGE
        # -----------------------------------------------------
        min_price = filters.get("min_price")
        max_price = filters.get("max_price")

        if min_price:
            qs = qs.filter(
                variants__price__gte=min_price
            )

        if max_price:
            qs = qs.filter(
                variants__price__lte=max_price
            )

        # -----------------------------------------------------
        # STOCK
        # -----------------------------------------------------
        in_stock = filters.get("in_stock")

        if in_stock:
            qs = qs.filter(
                variants__stock_quantity__gt=0
            )

        # -----------------------------------------------------
        # SORTING
        # -----------------------------------------------------
        ordering = filters.get("ordering")

        allowed_ordering = [
            "created_at",
            "-created_at",
            "title",
            "-title",
            "average_rating",
            "-average_rating",
            "total_sold",
            "-total_sold",
        ]

        if ordering in allowed_ordering:
            qs = qs.order_by(ordering)

        else:
            qs = qs.order_by("-created_at")

        return qs