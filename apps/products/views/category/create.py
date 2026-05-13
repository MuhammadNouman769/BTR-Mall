from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser


from apps.products.serializers.request.categories_request_serializers.category_request import CategoryCreateUpdateSerializer
from apps.products.serializers.response.categories_response_serializers.category_response import CategorySerializer
from apps.products.services.category_service import CategoryService
from apps.products.schemas.category.create_schema import category_create_schema


class CategoryCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @category_create_schema
    def post(self, request):

        serializer = CategoryCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.create(
            request.user,
            serializer.validated_data
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )