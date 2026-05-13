from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.selectors.option_selector import ProductOptionSelector
from apps.products.serializers.response.option_response_serializers.option_response import ProductOptionResponseSerializer
from apps.products.schemas.option.detail_schema import option_detail_schema


class OptionDetailAPIView(APIView):

    @option_detail_schema
    def get(self, request, pk):
        option = ProductOptionSelector.detail(pk)
        serializer = ProductOptionResponseSerializer(option)

        return Response(serializer.data, status=status.HTTP_200_OK)