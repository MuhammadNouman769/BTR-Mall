from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.selectors.variant_selector import VariantSelector

from apps.products.serializers.response.variant_response import (
    ProductVariantResponseSerializer
)

from apps.products.schemas.variant.list_schema import (
    variant_list_schema
)


class VariantListAPIView(APIView):

    @variant_list_schema
    def get(self, request):

        variants = VariantSelector.list_variants()

        serializer = ProductVariantResponseSerializer(
            variants,
            many=True
        )

        return Response(serializer.data)