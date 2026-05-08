from django.urls import path
from apps.products.views.admin.shop_seller_restore import ShopRestoreRequestAPIView


urlpatterns = [ 
    path("shops/<int:id>/restore-request/", ShopRestoreRequestAPIView.as_view()),
]