# apps/products/views/product/update.py

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.common.enums import UserRoleChoices
from apps.products.models import Product
from apps.products.parsers.product_parser import (
    ProductRequestParser,
)
from apps.products.schemas.product.update_schema import (
    product_update_schema,
)
from apps.products.serializers.request.product_request_serializers.product_request import (
    ProductCreateSerializer,
)

from apps.products.services.product_service import (
    ProductService,
)


@extend_schema_view(
    put=product_update_schema,
    patch=product_update_schema,
)
class ProductUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = ProductRequestParser.parser_classes

    # =====================================================
    # PUT
    # =====================================================

    def put(self, request, pk):

        return self.update(
            request=request,
            pk=pk,
            partial=False,
        )

    # =====================================================
    # PATCH
    # =====================================================

    def patch(self, request, pk):

        return self.update(
            request=request,
            pk=pk,
            partial=True,
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, request, pk, partial=False):

        # -------------------------------------------------
        # ROLE VALIDATION
        # -------------------------------------------------

        if request.user.role != UserRoleChoices.SELLER:

            return Response(
                {
                    "error": "Only sellers can update products",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # -------------------------------------------------
        # GET PRODUCT
        # -------------------------------------------------

        try:

            product = Product.objects.get(
                pk=pk,
                shop=request.user.shop,
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "error": "Product not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # -------------------------------------------------
        # PARSE REQUEST
        # -------------------------------------------------

        data = ProductRequestParser.parse(request)

        # -------------------------------------------------
        # VALIDATE REQUEST
        # -------------------------------------------------

        serializer = ProductCreateSerializer(
            product,
            data=data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        # -------------------------------------------------
        # UPDATE PRODUCT
        # -------------------------------------------------

        product = ProductService.update_product(
            user=request.user,
            instance=product,
            validated_data=serializer.validated_data,
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product updated successfully.",
                "data": ProductDetailResponseSerializer(
                    product
                ).data,
            },
            status=status.HTTP_200_OK,
        )