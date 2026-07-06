from django.urls import path

from apps.products.views.variant_image.create import (
    VariantImageCreateAPIView,
)
from apps.products.views.variant_image.list import (
    VariantImageListAPIView,
)
from apps.products.views.variant_image.detail import (
    VariantImageDetailAPIView,
)
from apps.products.views.variant_image.update import (
    VariantImageUpdateAPIView,
)
from apps.products.views.variant_image.delete import (
    VariantImageDeleteAPIView,
)


urlpatterns = [
    path("",VariantImageListAPIView.as_view(),name="variant_image_list",),
    path("create/",VariantImageCreateAPIView.as_view(),name="variant-image-create",),
    path("<int:pk>/",VariantImageDetailAPIView.as_view(),name="variant_image_detail",),
    path("<int:pk>/update/",VariantImageUpdateAPIView.as_view(),name="variant-image-update",),
    path("<int:pk>/delete/",VariantImageDeleteAPIView.as_view(),name="variant-image-delete"),
]