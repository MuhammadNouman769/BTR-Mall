from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiTypes
)

from apps.products.serializers.request.product_resquest_serializers.product_request import (
    ProductCreateSerializer
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer
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

    request=ProductCreateSerializer,

    responses={
        201: ProductDetailResponseSerializer
    },

    examples=[

        OpenApiExample(
            name="Multipart Upload Example",
            value={
                "title": "iPhone 15 Pro",
                "short_description": "Latest Apple flagship phone",
                "description_html": "<p>Premium device</p>",
                "brand": "Apple",

                "categories": [1, 2],

                "images": "(file upload in form-data)",

                "options": [
                    {
                        "name": "Color",
                        "values": [{"value": "Black"}]
                    }
                ],

                "variants": [
                    {
                        "sku": "IP15-BLK-128",
                        "price": "250000",
                        "stock_quantity": 10,
                        "images": "(file upload in nested form-data)"
                    }
                ]
            }
        )
    ]
)