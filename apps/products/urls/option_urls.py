from django.urls import path

from apps.products.views.option.create import OptionCreateAPIView
from apps.products.views.option.update import OptionUpdateAPIView
from apps.products.views.option.list import OptionListAPIView
from apps.products.views.option.delete import OptionDeleteAPIView
from apps.products.views.option.detail import OptionDetailAPIView


urlpatterns = [
    path("",OptionListAPIView.as_view(),name="option-list",),
    path("create/",OptionCreateAPIView.as_view(),name="option-create",),
    path("<int:pk>/",OptionDetailAPIView.as_view(),name="option-detail",),
    path("<int:pk>/update/",OptionUpdateAPIView.as_view(),name="option-update",),
    path("<int:pk>/delete/",OptionDeleteAPIView.as_view(),name="option-delete",),
]