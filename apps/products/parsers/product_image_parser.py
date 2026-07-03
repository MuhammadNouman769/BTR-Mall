from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)


class ProductImageRequestParser:

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @classmethod
    def parse(cls, request):

        data = request.data.copy()

        if "alt_text" not in data:
            data["alt_text"] = ""

        if "position" not in data:
            data["position"] = 0

        return data