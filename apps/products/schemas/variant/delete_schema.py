from drf_spectacular.utils import extend_schema


variant_delete_schema = extend_schema(
    tags=["Variants"],

    summary="Delete Variant",

    description="Delete an existing product variant.",

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Variant deleted successfully."
                },
            },
        },
        404: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Variant not found."
                },
            },
        },
    },
)