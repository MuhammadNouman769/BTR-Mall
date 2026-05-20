from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False
    )

    # =====================================================
    # VALIDATE EMAIL
    # =====================================================

    def validate_email(self, value):

        return value.lower().strip()