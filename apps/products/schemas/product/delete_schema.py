from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

product_delete_schema = extend_schema(
    tags=["Products"],

    summary="Delete Product",

    description="""
    Seller can soft delete own product.
    Product status becomes DELETED.
    """,

    responses={
        200: OpenApiResponse(
            description="Product deleted successfully"
        ),

        403: OpenApiResponse(
            description="Permission denied"
        ),

        404: OpenApiResponse(
            description="Product not found"
        ),
    }
)