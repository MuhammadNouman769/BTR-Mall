from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.services.option_service import ProductOptionService
from apps.products.serializers.request.option_request_serializers.option_request import (
    ProductOptionCreateSerializer,
)
from apps.products.schemas.option.create_schema import (
    option_create_schema,
)


@extend_schema_view(
    post=option_create_schema,
)
class OptionCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ProductOptionCreateSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        option = ProductOptionService.create_option(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return Response(
            {
                "message": "Option created successfully",
                "id": option.id,
            },
            status=status.HTTP_201_CREATED,
        )