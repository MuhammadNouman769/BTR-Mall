from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.product_selector import ProductSelector
from apps.products.serializers.response.product_response_serializers.product_response import ProductDetailResponseSerializer
from apps.products.schemas.product.detail_schema import product_detail_schema


@extend_schema_view(
    get=product_detail_schema
)
class ProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        try:
            product = ProductSelector.detail(
                pk=pk,
                user=request.user
            )

        except Exception:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductDetailResponseSerializer(product)

        return Response(serializer.data)