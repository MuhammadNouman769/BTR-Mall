from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.product_image.detail_schema import (
    product_image_detail_schema,
)
from apps.products.selectors.product_image_selector import (
    ProductImageSelector,
)
from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
    ProductImageResponseSerializer,
)


@extend_schema_view(
    get=product_image_detail_schema,
)
class ProductImageDetailAPIView(APIView):

    permission_classes = [AllowAny]

    # =====================================================
    # DETAIL
    # =====================================================

    def get(self, request, pk):

        image = ProductImageSelector.detail(
            pk=pk,
        )

        serializer = ProductImageResponseSerializer(
            image,
        )

        return Response(
            {
                "message": "Product image fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )