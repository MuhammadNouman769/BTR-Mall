from rest_framework.exceptions import ValidationError

from apps.products.models import ProductOption

from apps.products.validators.product_validator import (
    ProductValidator,
)


class OptionValidator:

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def validate_create(
        cls,
        user,
        validated_data,
    ):

        product = validated_data["product"]

        ProductValidator.validate_owner(
            product,
            user,
        )

        cls.validate_option(
            validated_data,
        )

    # =====================================================
    # UPDATE
    # =====================================================

    @classmethod
    def validate_update(
        cls,
        user,
        instance,
        validated_data,
    ):

        ProductValidator.validate_owner(
            instance.product,
            user,
        )

        if "name" in validated_data:

            queryset = ProductOption.objects.filter(
                product=instance.product,
                name__iexact=validated_data["name"].strip(),
            ).exclude(
                pk=instance.pk,
            )

            if queryset.exists():

                raise ValidationError({
                    "name": "Option already exists."
                })

        if "values" in validated_data:

            cls.validate_values(
                validated_data["values"],
            )

    # =====================================================
    # OPTION
    # =====================================================

    @classmethod
    def validate_option(
        cls,
        validated_data,
    ):

        name = validated_data["name"].strip()

        product = validated_data["product"]

        if ProductOption.objects.filter(
            product=product,
            name__iexact=name,
        ).exists():

            raise ValidationError({
                "name": "Option already exists."
            })

        cls.validate_values(
            validated_data.get(
                "values",
                [],
            ),
        )

    # =====================================================
    # VALUES
    # =====================================================

    @staticmethod
    def validate_values(values):

        if not values:

            raise ValidationError({
                "values": (
                    "At least one value is required."
                )
            })

        value_names = set()

        for value in values:

            value_text = value.get(
                "value",
                "",
            ).strip()

            if not value_text:

                raise ValidationError({
                    "values": (
                        "Value cannot be empty."
                    )
                })

            lower_value = value_text.lower()

            if lower_value in value_names:

                raise ValidationError({
                    "values": (
                        f'Duplicate value "{value_text}" is not allowed.'
                    )
                })

            value_names.add(lower_value)