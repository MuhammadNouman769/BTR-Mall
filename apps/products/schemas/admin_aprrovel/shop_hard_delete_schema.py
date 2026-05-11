from drf_spectacular.utils import extend_schema


shop_hard_delete_schema = extend_schema(
    summary="Permanently delete shop (Admin)",
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "id": {"type": "integer"}
            }
        }
    }
)