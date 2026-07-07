from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.option.create_schema import (
    option_create_schema,
)
from apps.products.serializers.request.option_request_serializers.option_request import (
    ProductOptionCreateSerializer,
)
from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionResponseSerializer,
)
from apps.products.services.option_service import (
    ProductOptionService,
)


@extend_schema_view(
    post=option_create_schema,
)
class OptionCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # CREATE OPTION
    # =====================================================

    def post(self, request):

        serializer = ProductOptionCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        option = ProductOptionService.create_option(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            {
                "message": "Option created successfully.",
                "data": ProductOptionResponseSerializer(
                    option,
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )