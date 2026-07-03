import json

from rest_framework.exceptions import ValidationError

from rest_framework.parsers import (
    JSONParser,
    MultiPartParser,
    FormParser,
)


class ProductRequestParser:

    parser_classes = [
        JSONParser,
        MultiPartParser,
        FormParser,
    ]

    JSON_FIELDS = [
        "categories",
        "options",
        "variants",
    ]

    @classmethod
    def parse(cls, request):

        data = request.data.copy()

        # =====================================================
        # PARSE JSON FIELDS
        # =====================================================

        for field in cls.JSON_FIELDS:

            value = data.get(field)

            if value and isinstance(value, str):

                try:
                    data[field] = json.loads(value)

                except json.JSONDecodeError:

                    raise ValidationError({
                        field: "Invalid JSON format."
                    })

        return data