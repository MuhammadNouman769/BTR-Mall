from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from apps.users.serializers import VerifyOTPSerializer
from apps.users.services.otp_service import OTPService
from apps.users.services.auth_service import AuthService
from apps.users.schemas import verify_otp_schema

User = get_user_model()


class VerifyOTPAPIView(APIView):

    @verify_otp_schema
    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        # -------------------------------------------------
        # USER FETCH (SAFE WAY)
        # -------------------------------------------------
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # OTP VERIFY
        # -------------------------------------------------
        success, msg = OTPService.verify_otp(user, otp)

        if not success:
            return Response(
                {"error": msg},
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # ACTIVATE USER
        # -------------------------------------------------
        AuthService.activate_user(user)

        return Response(
            {
                "message": "Account verified successfully"
            },
            status=status.HTTP_200_OK
        )