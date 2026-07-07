from django.db import transaction

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)

from apps.products.validators.option_validator import (
    OptionValidator,
)


class ProductOptionService:

    # =====================================================
    # CREATE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_option(
        user,
        validated_data,
    ):

        OptionValidator.validate_create(
            user,
            validated_data,
        )

        values = validated_data.pop(
            "values",
        )

        option = ProductOption.objects.create(
            **validated_data,
        )

        ProductOptionValue.objects.bulk_create(
            [
                ProductOptionValue(
                    option=option,
                    value=value["value"].strip(),
                    position=value.get(
                        "position",
                        index + 1,
                    ),
                )
                for index, value in enumerate(values)
            ]
        )

        return option

    # =====================================================
    # UPDATE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def update_option(
        user,
        instance,
        validated_data,
    ):

        OptionValidator.validate_update(
            user,
            instance,
            validated_data,
        )

        values = validated_data.pop(
            "values",
            None,
        )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value,
            )

        instance.save()

        if values is not None:

            instance.values.all().delete()

            ProductOptionValue.objects.bulk_create(
                [
                    ProductOptionValue(
                        option=instance,
                        value=value["value"].strip(),
                        position=value.get(
                            "position",
                            index + 1,
                        ),
                    )
                    for index, value in enumerate(values)
                ]
            )

        return instance

    # =====================================================
    # DELETE
    # =====================================================

    @staticmethod
    @transaction.atomic
    def delete_option(
        user,
        instance,
    ):

        OptionValidator.validate_update(
            user,
            instance,
            {},
        )

        instance.delete()