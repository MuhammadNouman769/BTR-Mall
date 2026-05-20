from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.exceptions import ValidationError  # ← IMPORT THIS
from apps.products.models import Category
from apps.products.serializers.request.categories_request_serializers.category_request import CategoryCreateUpdateSerializer
from apps.products.serializers.response.categories_response_serializers.category_response import CategorySerializer
from apps.products.services.category_service import CategoryService
from apps.products.schemas.category.update_schema import category_update_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


class CategoryUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @category_update_schema
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategoryCreateUpdateSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = CategoryService.update(category, serializer.validated_data)
        except ValidationError as e:
          
            return Response(
                e.message_dict,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CategorySerializer(category).data, 
            status=status.HTTP_200_OK
        )