from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema_view

from apps.products.schemas.variant_image.create_schema import (
    variant_image_create_schema,
)
from apps.products.serializers.request.variant_image_request_serializers.variant_image_request import (
    VariantImageRequestSerializer,
)
from apps.products.serializers.response.variant_image_response_serializers.variant_image_response import (
    VariantImageDetailResponseSerializer,
)
from apps.products.services.variant_image_service import (
    VariantImageService,
)


@extend_schema_view(
    post=variant_image_create_schema,
)
class VariantImageCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # CREATE VARIANT IMAGE
    # =====================================================

    def post(self, request):

        serializer = VariantImageRequestSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        image = VariantImageService.create_image(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            VariantImageDetailResponseSerializer(
                {
                    "message": "Variant image created successfully.",
                    "data": image,
                }
            ).data,
            status=status.HTTP_201_CREATED,
        )