from drf_spectacular.utils import extend_schema, OpenApiExample
from apps.products.serializers.request.option_request_serializers.option_request import ProductOptionCreateSerializer


option_create_schema = extend_schema(
    request=ProductOptionCreateSerializer,
    responses={201: {"message": "Option created successfully"}},
    examples=[
        OpenApiExample(
            "Create Option",
            value={
                "product": 1,
                "name": "Color",
                "values": [
                    {"value": "Red"},
                    {"value": "Blue"},
                    {"value": "Green"}
                ]
            }
        )
    ]
)