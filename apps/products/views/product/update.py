from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import Product
from apps.products.serializers.request.product_request import ProductCreateSerializer
from apps.products.services.product_service import ProductService
from apps.products.schemas.product.update_schema import product_update_schema
from apps.common.enums import UserRoleChoices


@extend_schema_view(
    put=product_update_schema,
    patch=product_update_schema
)
class ProductUpdateAPIView(UpdateAPIView):

    serializer_class = ProductCreateSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserRoleChoices.SELLER:
            return Product.objects.filter(shop=user.shop)

        return Product.objects.none()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        product = ProductService.create_product(
            user=request.user,
            validated_data=serializer.validated_data
        )

        return Response(
            {
                "message": "Product updated successfully",
                "id": product.id
            },
            status=status.HTTP_200_OK
        )