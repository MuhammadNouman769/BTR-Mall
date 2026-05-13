from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import Product

from apps.products.serializers.request.product_resquest_serializers.product_request import (
    ProductCreateSerializer
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer
)

from apps.products.services.product_service import ProductService

from apps.products.schemas.product.update_schema import (
    product_update_schema
)

from apps.common.enums import UserRoleChoices


@extend_schema_view(
    put=product_update_schema,
    patch=product_update_schema
)
class ProductUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, id):

        return self.update(
            request,
            id,
            partial=False
        )

    def patch(self, request, id):

        return self.update(
            request,
            id,
            partial=True
        )

    def update(self, request, id, partial=False):

        # -----------------------------------------
        # Seller Validation
        # -----------------------------------------
        if request.user.role != UserRoleChoices.SELLER:
            return Response(
                {
                    "error": "Only sellers can update products"
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
        # Serializer
        # -----------------------------------------
        serializer = ProductCreateSerializer(
            product,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)

        # -----------------------------------------
        # Update Product
        # -----------------------------------------
        product = ProductService.update_product(
            instance=product,
            validated_data=serializer.validated_data
        )

        # -----------------------------------------
        # Response
        # -----------------------------------------
        return Response(
            {
                "message": "Product updated successfully",
                "data": ProductDetailResponseSerializer(
                    product
                ).data
            },
            status=status.HTTP_200_OK
        )