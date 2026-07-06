from django.urls import path

from apps.products.views.product.create import ProductCreateAPIView
from apps.products.views.product.list import ProductListAPIView
from apps.products.views.product.detail import ProductDetailAPIView
from apps.products.views.product.update import ProductUpdateAPIView
from apps.products.views.product.delete import ProductDeleteAPIView

urlpatterns = [
    path("",ProductListAPIView.as_view(),name="product-list",),
    path("create/",ProductCreateAPIView.as_view(),name="product-create",),
    path("<int:pk>/",ProductDetailAPIView.as_view(),name="product-detail",),
    path("<int:pk>/update/",ProductUpdateAPIView.as_view(),name="product-update",),
    path("<int:pk>/delete/",ProductDeleteAPIView.as_view(),name="product-delete",),
]