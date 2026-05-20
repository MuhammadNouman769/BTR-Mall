from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from apps.users.serializers import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
from apps.users.services.otp_service import OTPService
from apps.users.schemas import (
    forgot_password_schema,
    reset_password_schema
)

User = get_user_model()


# =====================================================
# FORGOT PASSWORD
# =====================================================
class ForgotPasswordAPIView(APIView):

    @forgot_password_schema
    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(
            email=email
        ).only("id").first()

        # SECURITY: always return same response
        if user:
            OTPService.send_otp(user)

        return Response(
            {
                "success": True,
                "message": "If email exists, OTP has been sent"
            },
            status=status.HTTP_200_OK
        )


# =====================================================
# RESET PASSWORD
# =====================================================
class ResetPasswordAPIView(APIView):

    @reset_password_schema
    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = User.objects.filter(
            email=data["email"]
        ).only("id").first()

        if not user:
            return Response(
                {
                    "success": False,
                    "error": "Invalid request"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # OTP verification
        success, msg = OTPService.verify_otp(
            user,
            data["otp"]
        )

        if not success:
            return Response(
                {
                    "success": False,
                    "error": msg
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # reset password
        user.set_password(data["password"])
        user.save(update_fields=["password"])

        return Response(
            {
                "success": True,
                "message": "Password reset successful"
            },
            status=status.HTTP_200_OK
        )