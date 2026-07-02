
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.variant_selector import ProductVariantSelector
from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantResponseInProductSerializer
)
from apps.products.schemas.variant.detail_schema import variant_detail_schema

extend_schema_view(
    detail=variant_detail_schema,
)
class ProductVariantDetailAPIView(APIView):

    @variant_detail_schema
    def get(self, request, pk):

        variant = ProductVariantSelector.detail(pk)
        if not variant:
            return Response(
                {"errors": "variant not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductVariantResponseInProductSerializer(variant)

        return Response(
            {
                "message": "Variant Fetched successfully",
                "data":serializer.data
            },
            status=status.HTTP_200_OK
        )