from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductImage
from apps.products.parsers.product_image_parser import (
    ProductImageRequestParser,
)
from apps.products.schemas.product_image.update_schema import (
    product_image_update_schema,
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
    put=product_image_update_schema,
    patch=product_image_update_schema,
)
class ProductImageUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = ProductImageRequestParser.parser_classes

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
        # GET IMAGE
        # -------------------------------------------------

        image = get_object_or_404(
            ProductImage,
            pk=pk,
        )

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
            image,
            data=data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        # -------------------------------------------------
        # UPDATE IMAGE
        # -------------------------------------------------

        image = ProductImageService.update_image(
            user=request.user,
            instance=image,
            validated_data=serializer.validated_data,
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product image updated successfully.",
                "data": ProductImageResponseSerializer(
                    image,
                ).data,
            },
            status=status.HTTP_200_OK,
        )