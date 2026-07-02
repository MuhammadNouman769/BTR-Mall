from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view
from apps.products.parsers.variant_parser import VariantRequestParser
from apps.products.services.variant_service import VariantService
from apps.products.schemas.variant.create_schema import variant_create_schema
from apps.products.serializers.request.variant_request_serializers.variant_request import (
    ProductVariantCreateSerializer,
)
@extend_schema_view(
    post=variant_create_schema,
)
class VariantCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = VariantRequestParser.parser_classes

    def post(self, request):

        data = VariantRequestParser.parse(
            request
        )
        serializer = ProductVariantCreateSerializer(
            data=data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        variant = VariantService.create_variant(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return Response(
            {
                "message": "Variant created successfully",
                "id": variant.id,
            },
            status=status.HTTP_201_CREATED,
        )