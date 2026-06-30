from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiRequest,
)

from apps.products.serializers.request.product_resquest_serializers.product_request import (
    ProductCreateSerializer,
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer,
)


product_create_schema = extend_schema(
    tags=["Products"],
    summary="Create Product",
    description="""
Create a complete ecommerce product with:

- Basic product information
- Category mapping
- Product images (file upload)
- Product options
- Product variants
- Variant images (file upload)
""",

    request=OpenApiRequest(
        request=ProductCreateSerializer,
        encoding={
            "images": {"contentType": "image/*"},
            "variants": {"contentType": "application/json"},
            "options": {"contentType": "application/json"},
        },
    ),

    responses={
        201: ProductDetailResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Multipart Form Data",
            request_only=True,
            value={
                "title": "iPhone 15 Pro",
                "short_description": "Latest Apple flagship phone",
                "description_html": "<p>Premium device</p>",
                "brand": "Apple",
                "categories": [1, 2],
                "images": [
                    {
                        "image": "<FILE>",
                        "alt_text": "Front View",
                        "position": 1,
                    }
                ],
                "options": [
                    {
                        "name": "Color",
                        "values": [
                            {
                                "value": "Black"
                            }
                        ]
                    }
                ],
                "variants": [
                    {
                        "sku": "IP15-BLK-128",
                        "price": "250000",
                        "stock_quantity": 10,
                        "images": [
                            {
                                "image": "<FILE>"
                            }
                        ],
                    }
                ],
            },
        ),
    ],
)