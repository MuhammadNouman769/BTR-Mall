from django.urls import path

from apps.products.views.review.create import ProductReviewCreateAPIView
from apps.products.views.review.list import ProductReviewListAPIView
from apps.products.views.review.detail import ProductReviewDetailAPIView
from apps.products.views.review.update import ProductReviewUpdateAPIView
from apps.products.views.review.delete import ProductReviewDeleteAPIView
from apps.products.views.review.image_delete import ProductReviewImageDeleteAPIView


urlpatterns = [

    path("reviews/create/",ProductReviewCreateAPIView.as_view()),
    path("reviews/",ProductReviewListAPIView.as_view()),
    path("reviews/<int:id>/update/",ProductReviewUpdateAPIView.as_view()),
    path("reviews/<int:id>/update/",ProductReviewUpdateAPIView.as_view()),
    path("reviews/<int:id>/delete/",ProductReviewDeleteAPIView.as_view()),
    path("review-images/<int:id>/delete/",ProductReviewImageDeleteAPIView.as_view()),
]