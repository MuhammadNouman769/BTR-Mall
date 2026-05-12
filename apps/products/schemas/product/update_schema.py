from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.product_request import ProductCreateSerializer


product_update_schema = extend_schema(
    tags=["Products"],
    summary="Update Product",
    request=ProductCreateSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Product updated successfully"},
                "id": {"type": "integer", "example": 1}
            }
        }
    },
    examples=[
        OpenApiExample(
            "Update Product Example",
            value={
                "title": "iPhone 15 Pro Max",
                "short_description": "Updated version",
                "description_html": "<p>Updated product</p>",
                "categories": [1],
                "brand": "Apple",
                "is_featured": True,
                "images": [
                    {
                        "image": "file.jpg",
                        "alt_text": "main image"
                    }
                ],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Black", "White"]
                    }
                ],
                "variants": [
                    {
                        "sku": "IP15-PM-BLK",
                        "price": 250000
                    }
                ]
            }
        )
    ]
)