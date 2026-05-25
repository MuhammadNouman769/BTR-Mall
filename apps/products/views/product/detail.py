from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer
)

from apps.products.schemas.product.detail_schema import (
    product_detail_schema
)

from apps.products.selectors.product_selector import (
    ProductSelector
)


@extend_schema_view(
    get=product_detail_schema
)
class ProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    # =====================================================
    # GET PRODUCT DETAIL
    # =====================================================

    def get(self, request, pk):

        # -------------------------------------------------
        # GET PRODUCT
        # -------------------------------------------------

        product = ProductSelector.detail(
            pk=pk,
            user=request.user
        )

        # -------------------------------------------------
        # NOT FOUND
        # -------------------------------------------------

        if not product:

            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # SERIALIZER
        # -------------------------------------------------

        serializer = ProductDetailResponseSerializer(
            product
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )