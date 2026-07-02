# apps/products/validators/option_validator.py

from rest_framework.exceptions import ValidationError


class OptionValidator:

    # =====================================================
    # VALIDATE OPTIONS
    # =====================================================

    @staticmethod
    def validate(options):

        if not options:
            return

        option_names = set()

        for option in options:

            name = option.get("name", "").strip()

            # -----------------------------------------
            # OPTION NAME
            # -----------------------------------------

            if not name:
                raise ValidationError({
                    "options": "Option name is required."
                })

            lower_name = name.lower()

            if lower_name in option_names:
                raise ValidationError({
                    "options": (
                        f'Duplicate option "{name}" is not allowed.'
                    )
                })

            option_names.add(lower_name)

            # -----------------------------------------
            # OPTION VALUES
            # -----------------------------------------

            values = option.get("values", [])

            if not values:
                raise ValidationError({
                    "options": (
                        f'Option "{name}" must contain at least one value.'
                    )
                })

            value_names = set()

            for value in values:

                value_text = (
                    value.get("value", "").strip()
                    if isinstance(value, dict)
                    else str(value).strip()
                )

                if not value_text:
                    raise ValidationError({
                        "options": (
                            f'Option "{name}" contains an empty value.'
                        )
                    })

                lower_value = value_text.lower()

                if lower_value in value_names:
                    raise ValidationError({
                        "options": (
                            f'Duplicate value "{value_text}" '
                            f'in option "{name}".'
                        )
                    })

                value_names.add(lower_value)