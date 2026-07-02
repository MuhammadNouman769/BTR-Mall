from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.selectors.option_selector import ProductOptionSelector
from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionResponseSerializer,
)
from apps.products.schemas.option.list_schema import option_list_schema
@extend_schema_view(
    get=option_list_schema,
)
class OptionListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        options = ProductOptionSelector.list()
        serializer = ProductOptionResponseSerializer(
            options,
            many=True,
        )
        return Response(
            {
                "message": "Options fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )