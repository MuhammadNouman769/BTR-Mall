from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductOption
from apps.products.services.option_service import ProductOptionService
from apps.products.schemas.option.delete_schema import option_delete_schema


class OptionDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @option_delete_schema
    def delete(self, request, pk):
        option = ProductOption.objects.get(pk=pk)
        ProductOptionService.delete_option(option)

        return Response({"message": "Option deleted successfully"})