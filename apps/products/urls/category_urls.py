from django.urls import path

from apps.products.views.category.create import CategoryCreateAPIView
from apps.products.views.category.list import CategoryListAPIView
from apps.products.views.category.detail import CategoryDetailAPIView
from apps.products.views.category.update import CategoryUpdateAPIView
from apps.products.views.category.delete import CategoryDeleteAPIView


urlpatterns = [
    path("",CategoryListAPIView.as_view(),name="category-list",),
    path("create/",CategoryCreateAPIView.as_view(),name="category-create",),
    path("<int:pk>/",CategoryDetailAPIView.as_view(),name="category-detail",),
    path("<int:pk>/update/",CategoryUpdateAPIView.as_view(),name="category-update",),
    path("<int:pk>/delete/",CategoryDeleteAPIView.as_view(),name="category-delete",),
]