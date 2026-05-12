"""
===============================================================
    URL configuration for core (Supply Chain / FootwareStore)
===============================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#  NEW: drf-spectacular imports
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


# ================= MAIN URLS =====================

urlpatterns = [
    path('admin/', admin.site.urls),

    # ================= USERS =================
    path('', include('apps.main.urls')),
    path('api/auth/', include('apps.users.urls')),

    # ================= PRODUCTS CORE =================
    path('api/shops/', include('apps.products.urls.shop_urls')),
    path('api/products/', include('apps.products.urls.product_urls')),
    path('api/categories/', include('apps.products.urls.category_urls')),
    path('api/variants/', include('apps.products.urls.variant_urls')),
    path('api/options/', include('apps.products.urls.option_urls')),
    path("api/reviews", include('apps.products.urls.review_urls')),

    # ================= SHOP MODULES =================

    # Admin + moderation + trash + restore
    path('api/shops/admin/', include('apps.products.urls.admin_urls')),

    # Verification flow
    path('api/shops/verification/', include('apps.products.urls.shop_verification_urls')),

    # Restore request system (seller → admin approval flow)
    path('api/shops/restore-requests/', include('apps.products.urls.seller_restore_request_urls')),

    # ================= SYSTEMS =================
    path('api/inventory/', include('apps.inventory_tracking.urls')),
    path('api/orders/', include('apps.order_fulfillment.urls')),
    path('api/shipments/', include('apps.shipment_monitoring.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/supply-chain/', include('apps.supplychain.urls')),

    # ================= DOCUMENTATION =================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
# ============ Static & Media Serving (Development Only) ============

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])