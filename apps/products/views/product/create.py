# apps/products/views/product/create.py

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema_view

from apps.products.services.product_service import ProductService

from apps.products.schemas.product.create_schema import (
    product_create_schema
)

from apps.products.serializers.request.product_resquest_serializers.product_request import (
    ProductCreateSerializer
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer
)


@extend_schema_view(
    post=product_create_schema
)
class ProductCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):

        data = request.data.copy()

        # =====================================================
        # PARSE JSON FIELDS
        # =====================================================

        json_fields = [
            "categories",
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

        # =====================================================
        # HANDLE PRODUCT IMAGES
        # =====================================================

        product_images = request.FILES.getlist("images")

        parsed_images = []

        for image in product_images:

            parsed_images.append({
                "image": image,
                "alt_text": "",
                "position": 0,
            })

        data["images"] = parsed_images

        # =====================================================
        # HANDLE VARIANT IMAGES
        # =====================================================

        variants = data.get("variants", [])

        for index, variant in enumerate(variants):

            variant_images = request.FILES.getlist(
                f"variants[{index}][images]"
            )

            parsed_variant_images = []

            for image in variant_images:

                parsed_variant_images.append({
                    "image": image,
                    "alt_text": "",
                    "is_main": False,
                    "position": 0,
                })

            variant["images"] = parsed_variant_images

        # =====================================================
        # SERIALIZER
        # =====================================================

        serializer = ProductCreateSerializer(
            data=data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # =====================================================
        # CREATE PRODUCT
        # =====================================================

        product = ProductService.create_product(
            user=request.user,
            validated_data=serializer.validated_data
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        return Response(
            {
                "message": "Product created successfully",
                "data": ProductDetailResponseSerializer(
                    product
                ).data
            },
            status=status.HTTP_201_CREATED
        )