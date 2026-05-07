
from django.urls import path

from apps.products.views.shop.create import ShopCreateAPIView
from apps.products.views.shop.list import ShopListAPIView
from apps.products.views.shop.detail import ShopDetailAPIView
from apps.products.views.shop.update import ShopUpdateAPIView
from apps.products.views.shop.delete import ShopDeleteAPIView


urlpatterns = [
    path("shops/create/", ShopCreateAPIView.as_view()),
    path("shops/list/", ShopListAPIView.as_view()),
    path("shops/<int:id>/", ShopDetailAPIView.as_view()),
    path("shops/<int:id>/update/", ShopUpdateAPIView.as_view()),
    path("shops/<int:id>/delete/", ShopDeleteAPIView.as_view()),
]