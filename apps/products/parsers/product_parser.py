import json

from rest_framework.exceptions import ValidationError

from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

class ProductRequestParser:

    parser_classes = [
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

        # =====================================================
        # PRODUCT IMAGES
        # =====================================================

        product_images = request.FILES.getlist(
            "images"
        )

        if product_images:

            data["images"] = [
                {
                    "image": image,
                    "alt_text": "",
                    "position": index,
                }
                for index, image in enumerate(product_images)
            ]

        # =====================================================
        # VARIANT IMAGES
        # =====================================================

        variants = data.get(
            "variants",
            [],
        )

        if isinstance(variants, list):

            for index, variant in enumerate(variants):

                images = request.FILES.getlist(
                    f"variants[{index}][images]"
                )

                if images:

                    variant["images"] = [
                        {
                            "image": image,
                            "alt_text": "",
                            "is_main": False,
                            "position": position,
                        }
                        for position, image in enumerate(images)
                    ]

        return data