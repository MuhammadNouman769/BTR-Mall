from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework import status
from drf_spectacular.utils import extend_schema_view
from apps.products.models import Category
from apps.products.services.category_service import CategoryService
from apps.products.serializers.request.categories_request_serializers.category_request import (
    CategoryCreateUpdateSerializer,
)
from apps.products.serializers.response.categories_response_serializers.category_response import (
    CategorySerializer,
)
from apps.products.schemas.category.update_schema import (
    category_update_schema,
)

@extend_schema_view(
    put=category_update_schema,
)
class CategoryUpdateAPIView(APIView):

    permission_classes = [IsAdminUser]
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def put(self, request, pk):

        category = get_object_or_404(
            Category,
            pk=pk,
        )
        serializer = CategoryCreateUpdateSerializer(
            category,
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        category = CategoryService.update(
            instance=category,
            validated_data=serializer.validated_data,
        )
        return Response(
            {
                "message": "Category updated successfully",
                "data": CategorySerializer(
                    category
                ).data,
            },
            status=status.HTTP_200_OK,
        )