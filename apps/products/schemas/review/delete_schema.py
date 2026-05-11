from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)


review_delete_schema = extend_schema(

    tags=["Product Reviews"],

    summary="Delete Review",

    description="""
    User can soft delete own review.
    """,

    responses={

        200: OpenApiResponse(
            description="Review deleted successfully"
        ),

        404: OpenApiResponse(
            description="Review not found"
        ),
    }
)