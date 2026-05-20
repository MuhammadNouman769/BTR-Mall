from rest_framework import serializers


class LogoutRequestSerializer(serializers.Serializer):

    refresh = serializers.CharField(
        required=True,
        help_text="Refresh token required to blacklist/logout user"
    )

    # =====================================================
    # VALIDATION
    # =====================================================
    def validate_refresh(self, value):

        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Invalid refresh token"
            )

        return value.strip()