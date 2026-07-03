from django.urls import path

from apps.products.views.product_image.create import ProductImageCreateAPIView
from apps.products.views.product_image.update import ProductImageUpdateAPIView
from apps.products.views.product_image.list import ProductImageListAPIView
from apps.products.views.product_image.detail import ProductImageDetailAPIView
from apps.products.views.product_image.delete import ProductImageDeleteAPIView


urlpatterns = [

    path("",ProductImageListAPIView.as_view(),),
    path("create/",ProductImageCreateAPIView.as_view(),),
    path("<int:pk>/",ProductImageDetailAPIView.as_view(),),
    path("<int:pk>/update/",ProductImageUpdateAPIView.as_view(),),
    path("<int:pk>/delete/",ProductImageDeleteAPIView.as_view(),),
]