from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from apps.products.serializers.request.product_request import ProductCreateSerializer


product_create_schema = extend_schema(
    tags=["Products"],
    summary="Create Product",
    description="""
Create a new product with full details including:
- Basic info (title, description)
- Categories
- Images
- Options (like color, size)
- Variants (SKU combinations)
""",

    request=ProductCreateSerializer,

    responses={
        201: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Product created successfully"
                    },
                    "id": {
                        "type": "integer",
                        "example": 1
                    }
                }
            },
            description="Product created successfully"
        )
    },

    examples=[
        OpenApiExample(
            name="Create Product Example",
            summary="Full product creation payload",
            description="Example showing how to create a product with categories, images, options and variants",
            value={
                "title": "iPhone 15 Pro",
                "short_description": "Latest Apple iPhone with advanced features",
                "description_html": "<p>Best phone ever</p>",

                "category_ids": [1, 2],

                "brand": "Apple",

                "product_status": "draft",

                "is_featured": True,
                "is_best_seller": False,
                "is_new": True,
                "is_on_sale": False,

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
                        "values": ["Black", "White"]
                    },
                    {
                        "name": "Storage",
                        "values": ["128GB", "256GB"]
                    }
                ],

                "variants": [
                    {
                        "sku": "IP15-BLK-128",
                        "price": 250000,
                        "stock_quantity": 10
                    }
                ]
            }
        )
    ]
)