from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

from apps.products.serializers.request.option_request_serializers.option_request import (
    ProductOptionCreateSerializer,
)
from apps.products.serializers.response.option_response_serializers.option_response import (
    ProductOptionDetailResponseSerializer,
)


option_update_schema = extend_schema(

    operation_id="option_update",

    tags=["Options"],

    summary="Update Option",

    description="""
Update an existing product option and replace its values.
""",

    request=ProductOptionCreateSerializer,

    responses={
        200: ProductOptionDetailResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Update Color Option",

            request_only=True,

            value={
                "product": 5,
                "name": "Color",
                "position": 1,
                "values": [
                    {
                        "value": "Black",
                        "position": 1,
                    },
                    {
                        "value": "White",
                        "position": 2,
                    },
                    {
                        "value": "Blue",
                        "position": 3,
                    },
                ],
            },
        ),
    ],
)