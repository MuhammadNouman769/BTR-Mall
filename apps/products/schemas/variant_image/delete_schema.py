from drf_spectacular.utils import extend_schema


variant_image_delete_schema = extend_schema(
    operation_id="variant_image_delete",

    tags=["Variant Images"],

    summary="Delete Variant Image",

    description="""
Delete an existing variant image.
""",

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Variant image deleted successfully."
                },
            },
        },
        404: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Variant image not found."
                },
            },
        },
    },
)