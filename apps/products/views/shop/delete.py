from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.products.models import Shop
from apps.products.serializers.request.shop_create_request_serializers.delete import EmptySerializer


@extend_schema_view(
    delete=extend_schema(
        tags=["Shop"],
        summary="Delete Shop",
        request=None,
        responses={204: None}
    )
)
class ShopDeleteAPIView(DestroyAPIView):

    queryset = Shop.objects.all()
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)