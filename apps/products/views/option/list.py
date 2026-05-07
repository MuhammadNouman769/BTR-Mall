from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.serializers.response.option_response import ProductOptionResponseSerializer
from apps.products.selectors.option_selector import ProductOptionSelector
from apps.products.schemas.option.list_schema import option_list_schema


class OptionListAPIView(APIView):

    @option_list_schema
    def get(self, request):
        options = ProductOptionSelector.list()
        serializer = ProductOptionResponseSerializer(options, many=True)

        return Response(serializer.data)