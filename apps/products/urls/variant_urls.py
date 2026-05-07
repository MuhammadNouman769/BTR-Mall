from django.urls import path

from apps.products.views.variant.create import VariantCreateAPIView
from apps.products.views.variant.update import VariantUpdateAPIView
from apps.products.views.variant.list import VariantListAPIView
from apps.products.views.variant.delete import VariantDeleteAPIView


urlpatterns = [
    path("variants/create/", VariantCreateAPIView.as_view()),
    path("variants/<int:pk>/update/", VariantUpdateAPIView.as_view()),
    path("variants/list/", VariantListAPIView.as_view()),
    path("variants/<int:pk>/delete/", VariantDeleteAPIView.as_view()),
]