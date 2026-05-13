from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductOption
from apps.products.serializers.request.option_request_serializers.option_request import ProductOptionCreateSerializer
from apps.products.services.option_service import ProductOptionService
from apps.products.schemas.option.update_schema import option_update_schema


class OptionUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @option_update_schema
    def put(self, request, pk):
        option = ProductOption.objects.get(pk=pk)

        serializer = ProductOptionCreateSerializer(option, data=request.data)
        serializer.is_valid(raise_exception=True)

        ProductOptionService.update_option(option, serializer.validated_data)

        return Response({"message": "Option updated successfully",
                         "id": option.id}
                        )