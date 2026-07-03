# apps/products/views/product/create.py

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.parsers.product_parser import (
    ProductRequestParser,
)
from apps.products.schemas.product.create_schema import (
    product_create_schema,
)
from apps.products.serializers.request.product_request_serializers.product_request import (
    ProductCreateSerializer,
)
from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer,
)
from apps.products.services.product_service import (
    ProductService,
)


@extend_schema_view(
    post=product_create_schema,
)
class ProductCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = ProductRequestParser.parser_classes

    # =====================================================
    # CREATE PRODUCT
    # =====================================================

    def post(self, request):

        # -------------------------------------------------
        # PARSE REQUEST
        # -------------------------------------------------

        data = ProductRequestParser.parse(request)

        # -------------------------------------------------
        # VALIDATE REQUEST
        # -------------------------------------------------

        serializer = ProductCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # -------------------------------------------------
        # CREATE PRODUCT
        # -------------------------------------------------

        product = ProductService.create_product(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product created successfully.",
                "data": ProductDetailResponseSerializer(
                    product
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )