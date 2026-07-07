from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.option.detail_schema import (
    option_detail_schema,
)
from apps.products.selectors.option_selector import (
    ProductOptionSelector,
)
from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionDetailResponseSerializer,
)


@extend_schema_view(
    get=option_detail_schema,
)
class OptionDetailAPIView(APIView):

    permission_classes = [AllowAny]

    # =====================================================
    # DETAIL OPTION
    # =====================================================

    def get(self, request, pk):

        option = get_object_or_404(
            ProductOptionSelector.detail(pk),
        )

        return Response(
            {
                "message": "Option fetched successfully.",
                "data": ProductOptionDetailResponseSerializer(
                    option,
                ).data,
            },
            status=status.HTTP_200_OK,
        )