# admin_urls.py
from django.urls import path

from apps.products.views.admin.shop_trash_list import ShopTrashListAPIView
from apps.products.views.admin.shop_hard_delete import AdminShopHardDeleteAPIView
from apps.products.views.admin.shop_restore_approve import ApproveShopRestoreAPIView
from apps.products.views.admin.shop_restore_request import ShopRestoreRequestListAPIView
from apps.products.views.admin.shop_restore_request_detail import ShopRestoreRequestDetailAPIView

urlpatterns = [
    # restore system
    path("restore-requests/", ShopRestoreRequestListAPIView.as_view()),
    path("restore-requests/<int:id>/", ShopRestoreRequestDetailAPIView.as_view()),
    path("restore-requests/<int:id>/approve/", ApproveShopRestoreAPIView.as_view()),

    # trash system
    path("trash/", ShopTrashListAPIView.as_view()),

    # hard delete
    path("<int:id>/hard-delete/", AdminShopHardDeleteAPIView.as_view()),
]