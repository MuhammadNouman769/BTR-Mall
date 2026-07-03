from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.parsers.product_image_parser import (
    ProductImageRequestParser,
)
from apps.products.schemas.product_image.create_schema import (
    product_image_create_schema,
)
from apps.products.serializers.request.product_image_request_serializers.product_image_request import (
    ProductImageCreateSerializer,
)
from apps.products.serializers.response.product_image_response_serializers.product_image_response import (
    ProductImageResponseSerializer,
)
from apps.products.services.product_image_service import (
    ProductImageService,
)


@extend_schema_view(
    post=product_image_create_schema,
)
class ProductImageCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = ProductImageRequestParser.parser_classes

    # =====================================================
    # CREATE PRODUCT IMAGE
    # =====================================================

    def post(self, request):

        # -------------------------------------------------
        # PARSE REQUEST
        # -------------------------------------------------

        data = ProductImageRequestParser.parse(
            request,
        )

        # -------------------------------------------------
        # SERIALIZER
        # -------------------------------------------------

        serializer = ProductImageCreateSerializer(
            data=data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        # -------------------------------------------------
        # CREATE IMAGE
        # -------------------------------------------------

        image = ProductImageService.create_image(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product image created successfully.",
                "data": ProductImageResponseSerializer(
                    image,
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )