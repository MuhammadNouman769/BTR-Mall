from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

from apps.products.serializers.request.product_request_serializers.product_request import (
    ProductCreateSwaggerSerializer,
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

JSON Fields (sent as strings):
- categories: [1, 2]
- options: JSON string
- variants: JSON string

File Fields:
- images (multiple files)
- variants[0][images]
- variants[1][images]
- ...
""",

    request=ProductCreateSwaggerSerializer,

    responses={
        201: ProductDetailResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Create Product Example",
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
  }
]
""",

                "variants": """
[
  {
    "sku": "IP15-BLK-128",
    "price": "250000",
    "stock_quantity": 10
  }
]
""",
            },
        )
    ],
)