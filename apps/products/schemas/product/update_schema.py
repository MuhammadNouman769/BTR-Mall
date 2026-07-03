from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from apps.products.serializers.request.product_request_serializers.product_request import (
    ProductCreateSerializer
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    ProductDetailResponseSerializer
)


product_update_schema = extend_schema(

    tags=["Products"],

    summary="Update Product",

    description="""
Update an existing ecommerce product.

Seller can update:
- Basic information
- Categories
- Product images
- Variant images
- Product options
- Product variants
- SEO metadata
- Inventory
""",

    request={
        "multipart/form-data": ProductCreateSerializer
    },

    responses={
        200: OpenApiResponse(
            response=ProductDetailResponseSerializer,
            description="Product updated successfully"
        )
    },

    examples=[

        OpenApiExample(

            name="Update Product Example",

            summary="Complete product update payload",

            value={

                "title": "iPhone 15 Pro Max",

                "short_description": "Updated flagship iPhone",

                "description_html": "<p>Updated product description</p>",

                "brand": "Apple",

                "meta_title": "Updated iPhone",

                "meta_description": "Updated SEO description",

                "meta_keywords": "iphone, apple",

                "is_featured": True,

                "is_best_seller": True,

                "is_new": False,

                "is_on_sale": True,

                "category_ids": [1, 2],

                "images": [
                    {
                        "image": "(binary file)",
                        "alt_text": "Main Image",
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
                    }
                ],

                "variants": [

                    {
                        "sku": "IP15PM-BLK",

                        "barcode": "123456789",

                        "price": "250000.00",

                        "compare_at_price": "270000.00",

                        "stock_quantity": 20,

                        "track_inventory": True,

                        "allow_backorder": False,

                        "images": [
                            {
                                "image": "(binary file)",
                                "alt_text": "Variant Front",
                                "is_main": True,
                                "position": 1
                            }
                        ]
                    }
                ]
            },

            request_only=True,
        )
    ]
)