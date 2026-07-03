from drf_spectacular.utils import extend_schema


option_delete_schema = extend_schema(
    operation_id="option_delete",
    responses={200: {"message": "Option deleted successfully"}}
)