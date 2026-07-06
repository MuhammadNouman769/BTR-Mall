from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.variant.list_schema import (
    variant_list_schema,
)
from apps.products.selectors.variant_selector import (
    ProductVariantSelector,
)
from apps.products.serializers.response.variant_response_serializers.variant_response import (
    ProductVariantListResponseSerializer,
)


@extend_schema_view(
    get=variant_list_schema,
)
class VariantListAPIView(APIView):

    # =====================================================
    # LIST VARIANTS
    # =====================================================

    def get(self, request):

        variants = ProductVariantSelector.all()

        return Response(
            ProductVariantListResponseSerializer(
                {
                    "message": "Variants fetched successfully.",
                    "data": variants,
                }
            ).data,
            status=status.HTTP_200_OK,
        )