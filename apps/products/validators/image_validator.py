from rest_framework.exceptions import ValidationError


class ImageValidator:

    MAX_PRODUCT_IMAGES = 10
    MAX_VARIANT_IMAGES = 5

    # =====================================================
    # PRODUCT IMAGES
    # =====================================================

    @staticmethod
    def validate_product_images(images):

        if not images:
            return

        if len(images) > ImageValidator.MAX_PRODUCT_IMAGES:

            raise ValidationError({
                "images": (
                    f"Maximum "
                    f"{ImageValidator.MAX_PRODUCT_IMAGES} "
                    "product images are allowed."
                )
            })

        for image in images:

            if not image.get("image"):

                raise ValidationError({
                    "images": "Image file is required."
                })

    # =====================================================
    # VARIANT IMAGES
    # =====================================================

    @staticmethod
    def validate_variant_images(images):

        if not images:
            return

        if len(images) > ImageValidator.MAX_VARIANT_IMAGES:

            raise ValidationError({
                "images": (
                    f"Maximum "
                    f"{ImageValidator.MAX_VARIANT_IMAGES} "
                    "variant images are allowed."
                )
            })

        main_image_count = 0

        for image in images:

            if not image.get("image"):

                raise ValidationError({
                    "images": "Image file is required."
                })

            if image.get("is_main", False):

                main_image_count += 1

        if main_image_count > 1:

            raise ValidationError({
                "images": (
                    "Only one main image is allowed."
                )
            })