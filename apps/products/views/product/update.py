# apps/products/views/product/update.py

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from apps.products.models import Product

from apps.products.serializers.request.product_resquest_serializers.product_request import (
    ProductCreateSerializer
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer
)

from apps.products.services.product_service import ProductService

from apps.products.schemas.product.update_schema import (
    product_update_schema
)

from apps.common.enums import UserRoleChoices


@extend_schema_view(
    put=product_update_schema,
    patch=product_update_schema
)
class ProductUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    # =====================================================
    # PUT
    # =====================================================

    def put(self, request, id):

        return self.update(
            request=request,
            id=id,
            partial=False
        )

    # =====================================================
    # PATCH
    # =====================================================

    def patch(self, request, id):

        return self.update(
            request=request,
            id=id,
            partial=True
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, request, id, partial=False):

        # -------------------------------------------------
        # ROLE VALIDATION
        # -------------------------------------------------

        if request.user.role != UserRoleChoices.SELLER:

            return Response(
                {
                    "error": "Only sellers can update products"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------------------------------
        # GET PRODUCT
        # -------------------------------------------------

        try:

            product = Product.objects.get(
                id=id,
                shop=request.user.shop
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # COPY REQUEST DATA
        # -------------------------------------------------

        data = request.data.copy()

        # -------------------------------------------------
        # PARSE JSON FIELDS
        # -------------------------------------------------

        json_fields = [
            "category_ids",
            "options",
            "variants",
        ]

        for field in json_fields:

            value = data.get(field)

            if value and isinstance(value, str):

                try:

                    data[field] = json.loads(value)

                except json.JSONDecodeError:

                    return Response(
                        {
                            "error": f"Invalid JSON format for '{field}'"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # -------------------------------------------------
        # HANDLE PRODUCT IMAGES
        # -------------------------------------------------

        product_images = request.FILES.getlist("images")

        if product_images:

            parsed_images = []

            for image in product_images:

                parsed_images.append({
                    "image": image,
                    "alt_text": "",
                    "position": 0,
                })

            data["images"] = parsed_images

        # -------------------------------------------------
        # HANDLE VARIANT IMAGES
        # -------------------------------------------------

        variants = data.get("variants", [])

        for index, variant in enumerate(variants):

            variant_images = request.FILES.getlist(
                f"variants[{index}][images]"
            )

            if variant_images:

                parsed_variant_images = []

                for image in variant_images:

                    parsed_variant_images.append({
                        "image": image,
                        "alt_text": "",
                        "is_main": False,
                        "position": 0,
                    })

                variant["images"] = parsed_variant_images

        # -------------------------------------------------
        # SERIALIZER
        # -------------------------------------------------

        serializer = ProductCreateSerializer(
            product,
            data=data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        # -------------------------------------------------
        # UPDATE PRODUCT
        # -------------------------------------------------

        product = ProductService.update_product(
            instance=product,
            validated_data=serializer.validated_data
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return Response(
            {
                "message": "Product updated successfully",
                "data": ProductDetailResponseSerializer(
                    product
                ).data
            },
            status=status.HTTP_200_OK
        )