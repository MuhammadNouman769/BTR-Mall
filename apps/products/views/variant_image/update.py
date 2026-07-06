from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.models import VariantImage
from apps.products.schemas.variant_image.update_schema import (
    variant_image_update_schema,
)
from apps.products.serializers.request.variant_image_request_serializers.variant_image_request import (
    VariantImageRequestSerializer,
)
from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageDetailResponseSerializer,
)
from apps.products.services.variant_image_service import (
    VariantImageService,
)


@extend_schema_view(
    put=variant_image_update_schema,
    patch=variant_image_update_schema,
)
class VariantImageUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

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
    # UPDATE VARIANT IMAGE
    # =====================================================

    def update(self, request, pk, partial=False):

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

        serializer = VariantImageRequestSerializer(
            image,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        image = VariantImageService.update_image(
            user=request.user,
            instance=image,
            validated_data=serializer.validated_data,
        )

        return Response(
            VariantImageDetailResponseSerializer(
                {
                    "message": "Variant image updated successfully.",
                    "data": image,
                }
            ).data,
            status=status.HTTP_200_OK,
        )