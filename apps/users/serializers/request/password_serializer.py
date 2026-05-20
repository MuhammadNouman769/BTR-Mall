from rest_framework import serializers


# =========================================================
# FORGOT PASSWORD
# =========================================================
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()


# =========================================================
# RESET PASSWORD
# =========================================================
class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

    # -----------------------------------------
    # VALIDATE PASSWORD MATCH
    # -----------------------------------------
    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })

        return attrs

    def validate_email(self, value):
        return value.lower().strip()


# =========================================================
# VERIFY OTP
# =========================================================
class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate_email(self, value):
        return value.lower().strip()


# =========================================================
# RESEND OTP
# =========================================================
class ResendOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()