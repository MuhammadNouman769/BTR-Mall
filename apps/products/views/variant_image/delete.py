from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.models import VariantImage
from apps.products.schemas.variant_image.delete_schema import (
    variant_image_delete_schema,
)
from apps.products.services.variant_image_service import (
    VariantImageService,
)


@extend_schema_view(
    delete=variant_image_delete_schema,
)
class VariantImageDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # DELETE VARIANT IMAGE
    # =====================================================

    def delete(self, request, pk):

        try:

            image = VariantImage.objects.get(
                pk=pk,
            )

        except VariantImage.DoesNotExist:

            return Response(
                {
                    "error": "Variant image not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        VariantImageService.delete_image(
            user=request.user,
            instance=image,
        )

        return Response(
            {
                "message": "Variant image deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )