"""
===============================================================
    URL configuration for core (Supply Chain / FootwareStore)
===============================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ============================================================
# MAIN URLS
# ============================================================

urlpatterns = [

    # ========================================================
    # ADMIN
    # ========================================================

    path("admin/", admin.site.urls),

    # ========================================================
    # MAIN
    # ========================================================

    path("", include("apps.main.urls")),

    # ========================================================
    # AUTH
    # ========================================================

    path("api/auth/", include("apps.users.urls")),
    path("api/token/",TokenObtainPairView.as_view(),),
    path("api/token/refresh/",TokenRefreshView.as_view(),),

    # ========================================================
    # PRODUCTS
    # ========================================================

    path("api/products/",include("apps.products.urls.product_urls"),),
    path("api/product-images/",include("apps.products.urls.product_image_urls"),),
    path("api/categories/",include("apps.products.urls.category_urls"),),
    path("api/options/",include("apps.products.urls.option_urls"),),
    path("api/variants/",include("apps.products.urls.variant_urls"),),
    path("api/variant-images/",include("apps.products.urls.variant_image_urls"),),
    path("api/reviews/",include("apps.products.urls.review_urls"),),
    path("api/shops/",include("apps.products.urls.shop_urls"),),

    # ========================================================
    # SHOP MODULES
    # ========================================================

    path("api/shops/admin/",include("apps.products.urls.admin_urls"),),
    path("api/shops/verification/",include("apps.products.urls.shop_verification_urls"),),
    path("api/shops/restore-requests/",include("apps.products.urls.seller_restore_request_urls"),),

    # ========================================================
    # OTHER APPS
    # ========================================================

    path("api/inventory/",include("apps.inventory_tracking.urls"),),
    path("api/orders/",include("apps.order_fulfillment.urls"),),
    path("api/shipments/",include("apps.shipment_monitoring.urls"),),
    path("api/cart/",include("apps.cart.urls"),),
    path("api/supply-chain/",include("apps.supplychain.urls"),),

    # ========================================================
    # API DOCUMENTATION
    # ========================================================

    path("api/schema/",SpectacularAPIView.as_view(),name="schema",),
    path("api/swagger/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui",),
    path("api/redoc/",SpectacularRedocView.as_view(url_name="schema"),name="redoc",),
]
# ============================================================
# STATIC & MEDIA (Development Only)
# ============================================================

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT,)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS[0],)