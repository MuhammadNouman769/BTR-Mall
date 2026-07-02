from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import ProductOption
from apps.products.services.option_service import ProductOptionService
from apps.products.schemas.option.delete_schema import (
    option_delete_schema,
)

@extend_schema_view(
    delete=option_delete_schema,
)
class OptionDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        option = get_object_or_404(
            ProductOption,
            pk=pk,
        )
        ProductOptionService.delete_option(
            user=request.user,
            instance=option,
        )
        return Response(
            {
                "message": "Option deleted successfully",
            },
            status=status.HTTP_200_OK,
        )