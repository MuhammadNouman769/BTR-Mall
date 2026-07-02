from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductVariant
from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantResponseInProductSerializer
)
from apps.products.selectors.variant_selector import ProductVariantSelector
from apps.products.schemas.variant.list_schema import variant_list_schema

extend_schema_view(
    list=extend_schema_view,
)
class VariantListAPIView(APIView):

    @variant_list_schema
    def get(self, request):
        variants = ProductVariantSelector.all()
        serializer = ProductVariantResponseInProductSerializer(variants, many=True)

        return Response(
            {
                "message": "Variants fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )