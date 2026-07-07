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


option_create_schema = extend_schema(

    operation_id="option_create",

    tags=["Options"],

    summary="Create Option",

    description="""
Create a product option with multiple option values.

Example:

Color
- Black
- White
- Blue

Storage
- 128GB
- 256GB
""",

    request=ProductOptionCreateSerializer,

    responses={
        201: ProductOptionDetailResponseSerializer,
    },

    examples=[
        OpenApiExample(
            name="Create Color Option",

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
        OpenApiExample(
            name="Create Storage Option",

            request_only=True,

            value={
                "product": 5,
                "name": "Storage",
                "position": 2,
                "values": [
                    {
                        "value": "128GB",
                        "position": 1,
                    },
                    {
                        "value": "256GB",
                        "position": 2,
                    },
                    {
                        "value": "512GB",
                        "position": 3,
                    },
                ],
            },
        ),
    ],
)