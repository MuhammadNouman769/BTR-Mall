# apps/products/services/option_service.py

from django.db import transaction

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)

from apps.products.validators.product_validator import (
    ProductValidator,
)

from apps.products.validators.option_validator import (
    OptionValidator,
)


class ProductOptionService:

    # =====================================================
    # CREATE OPTION
    # =====================================================
    @staticmethod
    @transaction.atomic
    def create_option(user, validated_data):

        values = validated_data.pop("values", [])

        product = validated_data.get("product")

        ProductValidator.validate_owner(
            product,
            user,
        )

        OptionValidator.validate_values(
            values
        )

        option = ProductOption.objects.create(
            **validated_data
        )

        ProductOptionValue.objects.bulk_create([
            ProductOptionValue(
                option=option,
                value=value["value"].strip(),
                position=value.get(
                    "position",
                    index + 1,
                ),
            )
            for index, value in enumerate(values)
        ])

        return option

    # =====================================================
    # UPDATE OPTION
    # =====================================================
    @staticmethod
    @transaction.atomic
    def update_option(
        user,
        instance,
        validated_data,
    ):

        values = validated_data.pop(
            "values",
            None,
        )

        ProductValidator.validate_owner(
            instance.product,
            user,
        )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value,
            )

        instance.save()

        if values is not None:

            OptionValidator.validate_values(
                values
            )

            instance.values.all().delete()

            ProductOptionValue.objects.bulk_create([
                ProductOptionValue(
                    option=instance,
                    value=value["value"].strip(),
                    position=value.get(
                        "position",
                        index + 1,
                    ),
                )
                for index, value in enumerate(values)
            ])

        return instance

    # =====================================================
    # DELETE OPTION
    # =====================================================
    @staticmethod
    @transaction.atomic
    def delete_option(
        user,
        instance,
    ):

        ProductValidator.validate_owner(
            instance.product,
            user,
        )

        instance.delete()