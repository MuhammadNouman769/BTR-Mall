from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.services.category_service import CategoryService
from apps.products.serializers.request.categories_request_serializers.category_request import (
    CategoryCreateUpdateSerializer,
)
from apps.products.serializers.response.categories_response_serializers.category_response import (
    CategorySerializer,
)
from apps.products.schemas.category.create_schema import (
    category_create_schema,
)
@extend_schema_view(
    post=category_create_schema,
)

class CategoryCreateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = CategoryCreateUpdateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        category = CategoryService.create(
            validated_data=serializer.validated_data,
        )
        return Response(
            {
                "message": "Category created successfully",
                "data": CategorySerializer(
                    category
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )