from drf_spectacular.utils import extend_schema


variant_delete_schema = extend_schema(
    responses={200: {"message": "Variant deleted successfully"}}
)