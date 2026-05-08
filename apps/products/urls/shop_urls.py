# shops_urls.py
from django.urls import path
from apps.products.views.shop.create import ShopCreateAPIView
from apps.products.views.shop.detail import ShopDetailAPIView
from apps.products.views.shop.list import ShopListAPIView
from apps.products.views.shop.update import ShopUpdateAPIView
from apps.products.views.shop.delete import ShopDeleteAPIView


urlpatterns = [
    path("", ShopListAPIView.as_view()),          # GET all
    path("create/", ShopCreateAPIView.as_view()), # POST create
    path("<int:pk>/", ShopDetailAPIView.as_view()), # GET detail
    path("<int:pk>/update/", ShopUpdateAPIView.as_view()), # PATCH
    path("<int:pk>/delete/", ShopDeleteAPIView.as_view()), # soft delete
]