from django.urls import path

from apps.products.views.variant.create import VariantCreateAPIView
from apps.products.views.variant.update import VariantUpdateAPIView
from apps.products.views.variant.list import VariantListAPIView
from apps.products.views.variant.detail import ProductVariantDetailAPIView
from apps.products.views.variant.delete import VariantDeleteAPIView


urlpatterns = [
    path("",VariantListAPIView.as_view(),name="variant-list",),
    path("create/",VariantCreateAPIView.as_view(),name="variant-create",),
    path("<int:pk>/",ProductVariantDetailAPIView.as_view(),name="variant-detail",),
    path("<int:pk>/update/",VariantUpdateAPIView.as_view(),name="variant-update",),
    path("<int:pk>/delete/",VariantDeleteAPIView.as_view(),name="variant-delete",),
]