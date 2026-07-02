# apps/products/views/variant/update.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view
from apps.products.models import ProductVariant
from apps.products.parsers.variant_parser import VariantRequestParser

from apps.products.services.variant_service import VariantService
from apps.products.schemas.variant.update_schema import variant_update_schema
from apps.products.serializers.request.variant_request_serializers.variant_request import ProductVariantCreateSerializer

@extend_schema_view(
    put=variant_update_schema,
    patch=variant_update_schema,
)
class VariantUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = VariantRequestParser.parser_classes

    # =====================================================
    # PUT
    # =====================================================
    def put(self, request, pk):
        return self.update(
            request=request,
            pk=pk,
            partial=False,
        )

    # =====================================================
    # PATCH
    # =====================================================
    def patch(self, request, pk):
        return self.update(
            request=request,
            pk=pk,
            partial=True,
        )
    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, request, pk, partial=False):
        # -------------------------------------------------
        # GET VARIANT
        # -------------------------------------------------
        try:
            variant = ProductVariant.objects.get(
                pk=pk,
            )
        except ProductVariant.DoesNotExist:
            return Response(
                {
                    "error": "Variant not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # -------------------------------------------------
        # PARSE REQUEST
        # -------------------------------------------------
        data = VariantRequestParser.parse(
            request,
        )
        # -------------------------------------------------
        # SERIALIZER
        # -------------------------------------------------
        serializer = ProductVariantCreateSerializer(
            variant,
            data=data,
            partial=partial,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        # -------------------------------------------------
        # UPDATE VARIANT
        # -------------------------------------------------
        variant = VariantService.update_variant(
            user=request.user,
            instance=variant,
            validated_data=serializer.validated_data,
        )
        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------
        return Response(
            {
                "message": "Variant updated successfully",
                "id": variant.id,
            },
            status=status.HTTP_200_OK,
        )