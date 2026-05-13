from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

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
- Product options (Color, Size, etc.)
- Product variants (SKU, price, stock)
""",

    request=ProductCreateSerializer,

    responses={
        201: ProductDetailResponseSerializer
    },

    examples=[

        OpenApiExample(

            name="Create Product Example",

            summary="Full product creation example",

            value={

                "title": "iPhone 15 Pro",

                "short_description": "Latest Apple flagship phone",

                "description_html": "<p>Premium device</p>",

                "brand": "Apple",

                "is_featured": True,
                "is_best_seller": False,
                "is_new": True,
                "is_on_sale": False,

                "category_ids": [1, 2],

                "images": [
                    {
                        "image": "file.jpg",
                        "alt_text": "Front view",
                        "position": 1
                    }
                ],

                "options": [
                    {
                        "name": "Color",
                        "values": [
                            {"value": "Black"},
                            {"value": "White"}
                        ]
                    },
                    {
                        "name": "Storage",
                        "values": [
                            {"value": "128GB"},
                            {"value": "256GB"}
                        ]
                    }
                ],

                "variants": [
                    {
                        "sku": "IP15-BLK-128",
                        "barcode": "123456789",
                        "price": 250000,
                        "compare_at_price": 270000,
                        "stock_quantity": 10,
                        "track_inventory": True,
                        "allow_backorder": False
                    }
                ]
            }
        )
    ]
)