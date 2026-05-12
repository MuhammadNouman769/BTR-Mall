from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)


class ProductOptionService:

    # =====================================================
    #                   CREATE OPTION
    # =====================================================
    @staticmethod
    @transaction.atomic
    def create_option(user, validated_data):

        values_data = validated_data.pop("values", [])

        product = validated_data.get("product")

        # =========================================
        #           OWNERSHIP VALIDATION
        # =========================================
        if product.shop.owner != user:
            raise ValidationError({
                "error": "You cannot add options to this product"
            })

        # =========================================
        #         DUPLICATE VALUE CHECK
        # =========================================
        values = [v["value"].strip().lower() for v in values_data]

        if len(values) != len(set(values)):
            raise ValidationError({
                "error": "Duplicate option values are not allowed"
            })

        # =========================================
        #              CREATE OPTION
        # =========================================
        option = ProductOption.objects.create(
            **validated_data
        )

        # =========================================
        #           BULK CREATE VALUES
        # =========================================
        option_values = []

        for index, val in enumerate(values_data):

            option_values.append(
                ProductOptionValue(
                    option=option,
                    value=val["value"].strip(),
                    position=val.get("position", index + 1)
                )
            )

        ProductOptionValue.objects.bulk_create(
            option_values
        )

        return option

    # =====================================================
    #                  UPDATE OPTION
    # =====================================================
    @staticmethod
    @transaction.atomic
    def update_option(user, instance, validated_data):

        values_data = validated_data.pop("values", None)

        # =========================================
        #          OWNERSHIP VALIDATION
        # =========================================
        if instance.product.shop.owner != user:
            raise ValidationError({
                "error": "You cannot update this option"
            })

        # =========================================
        #             UPDATE FIELDS
        # =========================================
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # =========================================
        #             UPDATE VALUES
        # =========================================
        if values_data is not None:

            values = [
                v["value"].strip().lower()
                for v in values_data
            ]

            if len(values) != len(set(values)):
                raise ValidationError({
                    "error": "Duplicate option values are not allowed"
                })

            # remove old values
            instance.values.all().delete()

            # bulk create new values
            option_values = []

            for index, val in enumerate(values_data):

                option_values.append(
                    ProductOptionValue(
                        option=instance,
                        value=val["value"].strip(),
                        position=val.get(
                            "position",
                            index + 1
                        )
                    )
                )

            ProductOptionValue.objects.bulk_create(
                option_values
            )

        return instance

    # =====================================================
    #                  DELETE OPTION
    # =====================================================
    @staticmethod
    @transaction.atomic
    def delete_option(user, instance):

        # =========================================
        #          OWNERSHIP VALIDATION
        # =========================================
        if instance.product.shop.owner != user:
            raise ValidationError({
                "error": "You cannot delete this option"
            })

        instance.delete()