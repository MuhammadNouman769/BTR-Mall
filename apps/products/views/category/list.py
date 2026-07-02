from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_spectacular.utils import extend_schema_view
from apps.products.selectors.category_selector import CategorySelector
from apps.products.serializers.response.categories_response_serializers.category_response import (
    CategorySerializer,
)
from apps.products.schemas.category.list_schema import (
    category_list_schema,
)

@extend_schema_view(
    get=category_list_schema,
)
class CategoryListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        categories = CategorySelector.list()

        serializer = CategorySerializer(
            categories,
            many=True,
        )
        return Response(
            {
                "message": "Categories fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )