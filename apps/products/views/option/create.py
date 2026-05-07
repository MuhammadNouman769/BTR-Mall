from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.serializers.request.variant_request import (
    ProductVariantCreateSerializer
)

from apps.products.serializers.response.variant_response import (
    ProductVariantResponseSerializer
)

from apps.products.services.variant_service import VariantService

from apps.products.schemas.variant.create_schema import (
    variant_create_schema
)


class VariantCreateAPIView(APIView):

    @variant_create_schema
    def post(self, request):

        serializer = ProductVariantCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        variant = serializer.save()

        return Response(
            ProductVariantResponseSerializer(variant).data,
            status=status.HTTP_201_CREATED
        )