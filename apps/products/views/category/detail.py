from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_spectacular.utils import extend_schema_view
from apps.products.selectors.category_selector import CategorySelector
from apps.products.serializers.response.categories_response_serializers.category_response import (
    CategorySerializer,
)
from apps.products.schemas.category.detail_schema import (
    category_detail_schema,
)

@extend_schema_view(
    get=category_detail_schema,
)
class CategoryDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        category = CategorySelector.detail(
            pk=pk,
        )
        if not category:
            return Response(
                {
                    "error": "Category not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CategorySerializer(
            category,
        )
        return Response(
            {
                "message": "Category fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )