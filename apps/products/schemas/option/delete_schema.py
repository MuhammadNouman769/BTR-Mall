from drf_spectacular.utils import extend_schema


option_delete_schema = extend_schema(

    operation_id="option_delete",

    tags=["Options"],

    summary="Delete Option",

    description="""
Delete an existing product option along with all of its option values.
""",

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Option deleted successfully."
                },
            },
        },
        404: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Option not found."
                },
            },
        },
    },
)