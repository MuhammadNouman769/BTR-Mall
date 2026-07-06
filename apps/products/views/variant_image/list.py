from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.variant_image.list_schema import (
    variant_image_list_schema,
)
from apps.products.selectors.variant_image_selector import (
    VariantImageSelector,
)
from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageListResponseSerializer,
)


@extend_schema_view(
    get=variant_image_list_schema,
)
class VariantImageListAPIView(APIView):

    # =====================================================
    # LIST VARIANT IMAGES
    # =====================================================

    def get(self, request):

        images = VariantImageSelector.all()

        return Response(
            VariantImageListResponseSerializer(
                {
                    "message": "Variant images fetched successfully.",
                    "data": images,
                }
            ).data,
            status=status.HTTP_200_OK,
        )