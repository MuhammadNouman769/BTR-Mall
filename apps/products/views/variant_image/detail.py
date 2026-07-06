from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.variant_image.detail_schema import (
    variant_image_detail_schema,
)
from apps.products.selectors.variant_image_selector import (
    VariantImageSelector,
)
from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageDetailResponseSerializer,
)


@extend_schema_view(
    get=variant_image_detail_schema,
)
class VariantImageDetailAPIView(APIView):

    # =====================================================
    # DETAIL
    # =====================================================

    def get(self, request, pk):

        image = VariantImageSelector.detail(
            pk=pk,
        )

        if not image:

            return Response(
                {
                    "error": "Variant image not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            VariantImageDetailResponseSerializer(
                {
                    "message": "Variant image fetched successfully.",
                    "data": image,
                }
            ).data,
            status=status.HTTP_200_OK,
        )