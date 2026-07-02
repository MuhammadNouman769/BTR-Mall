# apps/products/parsers/variant_parser.py

from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)


class VariantRequestParser:

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @staticmethod
    def parse(request):

        data = request.data.copy()

        # =====================================================
        # HANDLE VARIANT IMAGES
        # =====================================================

        variant_images = request.FILES.getlist(
            "images"
        )

        if variant_images:

            parsed_images = []

            for index, image in enumerate(
                variant_images
            ):

                parsed_images.append(
                    {
                        "image": image,
                        "alt_text": "",
                        "is_main": index == 0,
                        "position": index + 1,
                    }
                )

            data["images"] = parsed_images

        return data