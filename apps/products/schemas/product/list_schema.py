from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from apps.products.serializers.response.product_response_serializers.product_response import (
    PaginatedProductResponseSerializer,
)


product_list_schema = extend_schema(

    tags=["Products"],

    summary="Product List",

    description="""
Retrieve a paginated list of products.

Supports filtering by query parameters.
""",

    parameters=[
        OpenApiParameter(
            name="page",
            type=int,
            required=False,
            description="Page number.",
        ),
        OpenApiParameter(
            name="page_size",
            type=int,
            required=False,
            description="Number of items per page.",
        ),
        OpenApiParameter(
            name="search",
            type=str,
            required=False,
            description="Search by product title.",
        ),
        OpenApiParameter(
            name="category",
            type=int,
            required=False,
            description="Filter by category ID.",
        ),
        OpenApiParameter(
            name="brand",
            type=str,
            required=False,
            description="Filter by brand.",
        ),
        OpenApiParameter(
            name="status",
            type=str,
            required=False,
            description="Filter by product status.",
        ),
    ],

    responses={
        200: PaginatedProductResponseSerializer,
    },
)