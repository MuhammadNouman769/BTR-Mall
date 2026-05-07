from apps.products.models import ProductOption, ProductOptionValue


class ProductOptionService:

    @staticmethod
    def create_option(validated_data):
        values_data = validated_data.pop("values", [])

        option = ProductOption.objects.create(**validated_data)

        for val in values_data:
            ProductOptionValue.objects.create(
                option=option,
                value=val["value"],
                position=val.get("position", 0)
            )

        return option

    @staticmethod
    def update_option(instance, validated_data):
        values_data = validated_data.pop("values", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if values_data is not None:
            instance.values.all().delete()

            for val in values_data:
                ProductOptionValue.objects.create(
                    option=instance,
                    value=val["value"],
                    position=val.get("position", 0)
                )

        return instance

    @staticmethod
    def delete_option(instance):
        instance.delete()