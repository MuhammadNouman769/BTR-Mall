from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.products.services.variant_service import VariantService
from apps.products.serializers.request.variant_request import ProductVariantCreateSerializer
from apps.products.schemas.variant.create_schema import variant_create_schema


class VariantCreateAPIView(APIView):

    @variant_create_schema
    def post(self, request):
        serializer = ProductVariantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant = VariantService.create_variant(serializer.validated_data)

        return Response(
            {"message": "Variant created successfully", "id": variant.id},
            status=status.HTTP_201_CREATED
        )