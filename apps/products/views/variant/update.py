from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.products.models import ProductVariant
from apps.products.services.variant_service import VariantService
from apps.products.serializers.request.variant_request import ProductVariantCreateSerializer
from apps.products.schemas.variant.update_schema import variant_update_schema


class VariantUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @variant_update_schema
    def put(self, request, pk):
        variant = ProductVariant.objects.get(pk=pk)

        serializer = ProductVariantCreateSerializer(variant, data=request.data)
        serializer.is_valid(raise_exception=True)

        variant = VariantService.update_variant(
            request.user,
            variant,
            serializer.validated_data)

        return Response({"message": "Variant updated successfully"})