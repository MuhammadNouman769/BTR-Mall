from drf_spectacular.utils import extend_schema
from apps.products.serializers.request.option_request_serializers.option_request import ProductOptionCreateSerializer


option_update_schema = extend_schema(
    request=ProductOptionCreateSerializer,
    responses={200: {"message": "Option updated successfully"}}
)