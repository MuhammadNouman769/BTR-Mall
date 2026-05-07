from django.urls import path

from apps.products.views.option.create import OptionCreateAPIView
from apps.products.views.option.update import OptionUpdateAPIView
from apps.products.views.option.list import OptionListAPIView
from apps.products.views.option.delete import OptionDeleteAPIView
from apps.products.views.option.detail import OptionDetailAPIView


urlpatterns = [
    path("options/create/", OptionCreateAPIView.as_view()),
    path("options/list/", OptionUpdateAPIView.as_view()),
    path("options/<int:pk>/", OptionDetailAPIView.as_view()),
    path("options/<int:pk>/update/", OptionUpdateAPIView.as_view()),
    path("options/list/", OptionListAPIView.as_view()),
    path("options/<int:pk>/delete/", OptionDeleteAPIView.as_view()),
]