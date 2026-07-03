from drf_spectacular.utils import extend_schema


product_image_delete_schema = extend_schema(
    operation_id="product_image_delete",

    tags=["Product Images"],

    summary="Delete Product Image",

    description="""
Delete a product image.
""",

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Product image deleted successfully.",
                }
            },
        },
    },
)