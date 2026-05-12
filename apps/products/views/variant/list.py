from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.models import ProductVariant
from apps.products.serializers.response.variant_response import ProductVariantResponseInProductSerializer
from apps.products.schemas.variant.list_schema import variant_list_schema


class VariantListAPIView(APIView):

    @variant_list_schema
    def get(self, request):
        variants = ProductVariant.objects.all()
        serializer = ProductVariantResponseInProductSerializer(variants, many=True)

        return Response(serializer.data)