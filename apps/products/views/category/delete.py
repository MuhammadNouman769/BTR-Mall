from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from drf_spectacular.utils import extend_schema_view
from apps.products.models import Category
from apps.products.services.category_service import CategoryService
from apps.products.schemas.category.delete_schema import (
    category_delete_schema,
)

@extend_schema_view(
    delete=category_delete_schema,
)
class CategoryDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        category = get_object_or_404(
            Category,
            pk=pk,
        )
        CategoryService.delete(
            instance=category,
        )
        return Response(
            {
                "message": "Category deleted successfully",
            },
            status=status.HTTP_200_OK,
        )