from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.variant.detail_schema import (
    variant_detail_schema,
)
from apps.products.selectors.variant_selector import (
    ProductVariantSelector,
)
from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantDetailResponseSerializer,
)


@extend_schema_view(
    get=variant_detail_schema,
)
class ProductVariantDetailAPIView(APIView):

    # =====================================================
    # GET VARIANT DETAIL
    # =====================================================

    def get(self, request, pk):

        variant = ProductVariantSelector.detail(
            pk=pk,
        )

        if not variant:

            return Response(
                {
                    "error": "Variant not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            ProductVariantDetailResponseSerializer(
                {
                    "message": "Variant fetched successfully.",
                    "data": variant,
                }
            ).data,
            status=status.HTTP_200_OK,
        )