# apps/products/validators/category_validator.py

from django.core.exceptions import ValidationError


class CategoryValidator:

    # =====================================================
    # VALIDATE CREATE
    # =====================================================

    @staticmethod
    def validate_create(validated_data):

        parent = validated_data.get("parent")

        if (
            parent and
            parent.pk == validated_data.get("id")
        ):
            raise ValidationError({
                "parent": (
                    "Category cannot be its own parent."
                )
            })

    # =====================================================
    # VALIDATE UPDATE
    # =====================================================

    @staticmethod
    def validate_update(instance, validated_data):

        parent = validated_data.get(
            "parent",
            instance.parent
        )

        if parent == instance:

            raise ValidationError({
                "parent": (
                    "Category cannot be parent of itself."
                )
            })

        CategoryValidator.validate_no_cycle(
            instance,
            parent
        )

    # =====================================================
    # VALIDATE DELETE
    # =====================================================

    @staticmethod
    def validate_delete(instance):

        if instance.children.exists():

            raise ValidationError({
                "error": (
                    "Cannot delete category with subcategories."
                )
            })

        if instance.products.exists():

            raise ValidationError({
                "error": (
                    "This category contains products. "
                    "Move or delete products first."
                )
            })

    # =====================================================
    # VALIDATE NO CYCLE
    # =====================================================

    @staticmethod
    def validate_no_cycle(instance, parent):

        current = parent

        while current:

            if current == instance:

                raise ValidationError({
                    "parent": (
                        "Circular category structure detected."
                    )
                })

            current = current.parent