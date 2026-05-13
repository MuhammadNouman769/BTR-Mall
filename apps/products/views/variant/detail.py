from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.selectors.variant_selector import ProductVariantSelector
from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantResponseSerializer
)
from apps.products.schemas.variant.detail_schema import variant_detail_schema


class ProductVariantDetailAPIView(APIView):

    @variant_detail_schema
    def get(self, request, pk):

        variant = ProductVariantSelector.detail(pk)

        serializer = ProductVariantResponseSerializer(variant)

        return Response(serializer.data)