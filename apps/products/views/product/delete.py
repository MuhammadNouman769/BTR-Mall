# apps/products/views/product/delete.py

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.common.enums import UserRoleChoices
from apps.products.models import Product
from apps.products.schemas.product.delete_schema import (
    product_delete_schema,
)
from apps.products.services.product_service import (
    ProductService,
)


@extend_schema_view(
    delete=product_delete_schema,
)
class ProductDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    def delete(self, request, pk):

        # -------------------------------------------------
        # ROLE VALIDATION
        # -------------------------------------------------

        if request.user.role != UserRoleChoices.SELLER:

            return Response(
                {
                    "error": "Only sellers can delete products.",
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
                    "error": "Product not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # -------------------------------------------------
        # DELETE PRODUCT
        # -------------------------------------------------

        ProductService.delete_product(
            user=request.user,
            instance=product,
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )