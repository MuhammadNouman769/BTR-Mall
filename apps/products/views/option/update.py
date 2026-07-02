from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductOption
from apps.products.services.option_service import ProductOptionService
from apps.products.serializers.request.option_request_serializers.option_request import (
    ProductOptionCreateSerializer,
)

from apps.products.schemas.option.update_schema import (
    option_update_schema,
)

@extend_schema_view(
    put=option_update_schema,
)
class OptionUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        option = get_object_or_404(
            ProductOption,
            pk=pk,
        )
        serializer = ProductOptionCreateSerializer(
            option,
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        option = ProductOptionService.update_option(
            user=request.user,
            instance=option,
            validated_data=serializer.validated_data,
        )
        return Response(
            {
                "message": "Option updated successfully",
                "id": option.id,
            },
            status=status.HTTP_200_OK,
        )