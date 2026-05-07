from drf_spectacular.utils import extend_schema


variant_delete_schema = extend_schema(
    summary="Delete Variant",

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Variant deleted successfully"
                }
            }
        }
    },

    tags=["Variants"]
)