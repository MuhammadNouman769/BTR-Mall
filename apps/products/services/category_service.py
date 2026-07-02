from django.db import transaction

from apps.products.models import Category

from apps.products.validators.category_validator import (
    CategoryValidator,
)


class CategoryService:

    # =====================================================
    # CREATE CATEGORY
    # =====================================================
    @staticmethod
    @transaction.atomic
    def create(validated_data):

        CategoryValidator.validate_create(
            validated_data
        )

        return Category.objects.create(
            **validated_data
        )

    # =====================================================
    # UPDATE CATEGORY
    # =====================================================
    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):

        CategoryValidator.validate_update(
            instance,
            validated_data,
        )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value,
            )

        instance.save()

        return instance

    # =====================================================
    # DELETE CATEGORY
    # =====================================================
    @staticmethod
    @transaction.atomic
    def delete(instance):

        CategoryValidator.validate_delete(
            instance
        )

        instance.delete()