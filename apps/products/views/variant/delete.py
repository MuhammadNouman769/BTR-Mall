
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.products.models import ProductVariant
from apps.products.services.variant_service import VariantService
from apps.products.schemas.variant.delete_schema import variant_delete_schema

@extend_schema_view(
    delete=variant_delete_schema
)
class VariantDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @variant_delete_schema
    def delete(self, request, pk):
        variant = get_object_or_404(
            ProductVariant,
            pk=pk
        )
        VariantService.delete_variant(
            request.user,
            variant
        )
        return Response(
            {
                "message": "Variant deleted successfully"
            },
            status=status.HTTP_200_OK
        )