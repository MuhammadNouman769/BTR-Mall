# apps/products/schemas/product/create_schema.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiRequest,
)

from apps.products.serializers.request.product_resquest_serializers.product_request import ProductCreateSerializer
from apps.products.serializers.response.product_response_serializers.product_response import ProductDetailResponseSerializer


product_create_schema = extend_schema(

    tags=["Products"],

    summary="Create Product",

    description="""
Create a complete ecommerce product with:

- Basic product information
- Category mapping
- Product images
- Product options
- Product variants
- Variant images
""",

    request=OpenApiRequest(

        request=ProductCreateSerializer,

        encoding={

            "images": {
                "style": "form",
                "explode": True
            },

            "variants": {
                "style": "form",
                "explode": True
            }
        }
    ),

    responses={
        201: ProductDetailResponseSerializer
    },

    examples=[

        OpenApiExample(

            name="Multipart Form Example",

            summary="Swagger multipart example",

            value={

                "title": "iPhone 15 Pro",

                "short_description": "Latest Apple flagship phone",

                "description_html": "<p>Premium device</p>",

                "brand": "Apple",

                "category_ids": [1, 2],

                "is_featured": True,

                "images": [
                    {
                        "image": "(binary)",
                        "alt_text": "Front view",
                        "position": 1
                    }
                ],

                "variants": [
                    {
                        "sku": "IP15-BLK-128",
                        "price": 250000,
                        "stock_quantity": 10,

                        "images": [
                            {
                                "image": "(binary)",
                                "alt_text": "Black variant",
                                "is_main": True
                            }
                        ]
                    }
                ]
            }
        )
    ]
)