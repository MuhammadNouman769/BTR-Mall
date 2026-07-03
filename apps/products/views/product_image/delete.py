from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductImage
from apps.products.schemas.product_image.delete_schema import (
    product_image_delete_schema,
)
from apps.products.services.product_image_service import (
    ProductImageService,
)


@extend_schema_view(
    delete=product_image_delete_schema,
)
class ProductImageDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, request, pk):

        image = get_object_or_404(
            ProductImage,
            pk=pk,
        )

        ProductImageService.delete_image(
            user=request.user,
            instance=image,
        )

        return Response(
            {
                "message": "Product image deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )