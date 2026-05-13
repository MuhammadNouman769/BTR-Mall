from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import Product

from apps.products.services.product_service import ProductService

from apps.products.schemas.product.delete_schema import (
    product_delete_schema
)

from apps.common.enums import UserRoleChoices


@extend_schema_view(
    delete=product_delete_schema
)
class ProductDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        # -----------------------------------------
        # Only Seller
        # -----------------------------------------
        if request.user.role != UserRoleChoices.SELLER:
            return Response(
                {
                    "error": "Only sellers can delete products"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------------------
        # Product Ownership Validation
        # -----------------------------------------
        try:
            product = Product.objects.get(
                id=id,
                shop=request.user.shop
            )

        except Product.DoesNotExist:
            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------------
        # Soft Delete
        # -----------------------------------------
        ProductService.delete_product(product)

        return Response(
            {
                "message": "Product deleted successfully"
            },
            status=status.HTTP_200_OK
        )