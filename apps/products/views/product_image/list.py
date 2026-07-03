from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.product_image.list_schema import (
    product_image_list_schema,
)
from apps.products.selectors.product_image_selector import (
    ProductImageSelector,
)
from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
    ProductImageResponseSerializer,
)


@extend_schema_view(
    get=product_image_list_schema,
)
class ProductImageListAPIView(APIView):

    permission_classes = [AllowAny]

    # =====================================================
    # LIST PRODUCT IMAGES
    # =====================================================

    def get(self, request):

        images = ProductImageSelector.list(
            filters=request.query_params,
        )

        serializer = ProductImageResponseSerializer(
            images,
            many=True,
        )

        return Response(
            {
                "message": "Product images fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )