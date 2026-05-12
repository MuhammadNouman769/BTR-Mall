# views/product/create.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view

from apps.common.enums import UserRoleChoices
from apps.products.serializers.request.product_request import ProductCreateSerializer
from apps.products.services.product_service import ProductService
from apps.products.schemas.product.create_schema import product_create_schema


@extend_schema_view(post=product_create_schema)
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # ================= SELLER VALIDATION =================
        if request.user.role != UserRoleChoices.SELLER:
            return Response(
                {"error": "Only sellers can create products"},
                status=status.HTTP_403_FORBIDDEN
            )

        # ================= SERIALIZER VALIDATION =================
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ================= SERVICE LAYER =================
        product = ProductService.create_product(
            user=request.user,
            validated_data=serializer.validated_data
        )

        # ================= RESPONSE =================
        return Response(
            {
                "message": "Product created successfully",
                "data": {
                    "id": product.id,
                    "title": product.title,
                    "status": product.product_status,
                }
            },
            status=status.HTTP_201_CREATED
        )