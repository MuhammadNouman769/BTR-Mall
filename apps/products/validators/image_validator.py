# apps/products/validators/image_validator.py

from rest_framework.exceptions import ValidationError


class ImageValidator:

    MAX_PRODUCT_IMAGES = 10
    MAX_VARIANT_IMAGES = 5

    # =====================================================
    # SINGLE PRODUCT IMAGE
    # =====================================================

    @staticmethod
    def validate_product_image(image):

        if image.get("image") is None:
            raise ValidationError({
                "image": "Image file is required."
            })

    # =====================================================
    # SINGLE VARIANT IMAGE
    # =====================================================

    @staticmethod
    def validate_variant_image(image):

        if image.get("image") is None:
            raise ValidationError({
                "image": "Image file is required."
            })

        if not isinstance(
            image.get("is_main", False),
            bool,
        ):
            raise ValidationError({
                "is_main": "Must be true or false."
            })

    # =====================================================
    # PRODUCT IMAGES
    # =====================================================

    @classmethod
    def validate_product_images(cls, images):

        if not images:
            return

        if len(images) > cls.MAX_PRODUCT_IMAGES:
            raise ValidationError({
                "images": (
                    f"Maximum {cls.MAX_PRODUCT_IMAGES} "
                    "product images are allowed."
                )
            })

        for image in images:
            cls.validate_product_image(image)

    # =====================================================
    # VARIANT IMAGES
    # =====================================================

    @classmethod
    def validate_variant_images(cls, images):

        if not images:
            return

        if len(images) > cls.MAX_VARIANT_IMAGES:
            raise ValidationError({
                "images": (
                    f"Maximum {cls.MAX_VARIANT_IMAGES} "
                    "variant images are allowed."
                )
            })

        main_image_count = 0

        for image in images:

            cls.validate_variant_image(image)

            if image.get("is_main", False):
                main_image_count += 1

        if main_image_count > 1:
            raise ValidationError({
                "images": (
                    "Only one main image is allowed."
                )
            })