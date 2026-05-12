from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.products.models import ProductVariant
from apps.products.services.variant_service import VariantService
from apps.products.schemas.variant.delete_schema import variant_delete_schema


class VariantDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @variant_delete_schema
    def delete(self, request, pk):
        variant = ProductVariant.objects.get(pk=pk)
        VariantService.delete_variant(
            request.user,
            variant
        )

        return Response({"message": "Variant deleted successfully"})