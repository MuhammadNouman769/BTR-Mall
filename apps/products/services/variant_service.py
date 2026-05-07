from apps.products.models import ProductVariant, VariantImage


class VariantService:

    @staticmethod
    def create_variant(validated_data):
        images_data = validated_data.pop("images", [])

        variant = ProductVariant.objects.create(**validated_data)

        for img in images_data:
            VariantImage.objects.create(
                variant=variant,
                image=img["image"],
                alt_text=img.get("alt_text", ""),
                is_main=img.get("is_main", False),
            )

        return variant

    @staticmethod
    def update_variant(instance, validated_data):
        images_data = validated_data.pop("images", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if images_data is not None:
            instance.variant_images.all().delete()

            for img in images_data:
                VariantImage.objects.create(
                    variant=instance,
                    image=img["image"],
                    alt_text=img.get("alt_text", ""),
                    is_main=img.get("is_main", False),
                )

        return instance

    @staticmethod
    def delete_variant(instance):
        instance.delete()