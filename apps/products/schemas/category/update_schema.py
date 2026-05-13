from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.products.serializers.request.categories_request_serializers.category_request import CategoryCreateUpdateSerializer
from apps.products.serializers.response.categories_response_serializers.category_response import CategorySerializer


category_update_schema = extend_schema(
    summary="Update Category",
    request=CategoryCreateUpdateSerializer,
    responses=CategorySerializer,
    tags=["Category"]
)