from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)


review_image_delete_schema = extend_schema(

    tags=["Product Reviews"],

    summary="Delete Review Image",

    description="""
    Delete a single review image.
    """,

    responses={

        200: OpenApiResponse(
            description="Image deleted successfully"
        ),

        404: OpenApiResponse(
            description="Image not found"
        ),
    }
)