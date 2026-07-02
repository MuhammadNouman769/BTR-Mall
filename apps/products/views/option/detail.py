from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.option_selector import ProductOptionSelector
from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionResponseSerializer,
)
from apps.products.schemas.option.detail_schema import (
    option_detail_schema,
)

@extend_schema_view(
    get=option_detail_schema,
)
class OptionDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        option = ProductOptionSelector.detail(pk)
        if not option:
            return Response(
                {
                    "error": "Option not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProductOptionResponseSerializer(
            option
        )
        return Response(
            {
                "message": "Option fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )