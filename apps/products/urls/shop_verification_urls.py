from django.urls import path

from apps.products.views.shop_verification.approve import ApproveShopAPIView
from apps.products.views.shop_verification.reject import RejectShopAPIView
from apps.products.views.shop_verification.list import PendingShopListAPIView



urlpatterns = [
    path("requests/", PendingShopListAPIView.as_view()),

    path("requests/<int:id>/approve/", ApproveShopAPIView.as_view()),
    path("requests/<int:id>/reject/", RejectShopAPIView.as_view()),
]