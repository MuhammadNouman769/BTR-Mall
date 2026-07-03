from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

from apps.products.serializers.request.product_request_serializers.product_request import (
    ProductCreateSerializer,
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer,
)


product_create_schema = extend_schema(

    operation_id="product_create",

    tags=["Products"],

    summary="Create Product",

    description="""
Create a new product.

Content-Type:
- multipart/form-data

JSON Fields:
- categories
- options
- variants

File Fields:
- images
- variants[0][images]
- variants[1][images]
- ...
""",

    request=ProductCreateSerializer,

    responses={
        201: ProductDetailResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Create Product",
            request_only=True,
            value={
                "title": "iPhone 15 Pro",
                "short_description": "Latest Apple flagship",
                "description_html": "<p>Premium smartphone</p>",
                "brand": "Apple",
                "categories": "[1,2]",
                "options": """
[
    {
        "name": "Color",
        "values": [
            {"value": "Black"},
            {"value": "Blue"}
        ]
    },
    {
        "name": "Storage",
        "values": [
            {"value": "128GB"},
            {"value": "256GB"}
        ]
    }
]
""",
                "variants": """
[
    {
        "sku": "IP15-BLK-128",
        "price": "250000",
        "stock_quantity": 10
    },
    {
        "sku": "IP15-BLU-256",
        "price": "280000",
        "stock_quantity": 5
    }
]
""",
            },
        )
    ],
)