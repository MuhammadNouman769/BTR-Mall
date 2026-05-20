from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from apps.users.serializers import ResendOTPSerializer
from apps.users.services.otp_service import OTPService
from apps.users.schemas import resend_otp_schema
from apps.users.services.user_service import UserService


User = get_user_model()


class ResendOTPAPIView(APIView):

    @resend_otp_schema
    def post(self, request):

        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # -----------------------------------------
        # USER FETCH FROM SERVICE
        # -----------------------------------------
        user = UserService.get_user_by_email(email)

        if not user:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------------
        # SEND OTP
        # -----------------------------------------
        success, msg = OTPService.send_otp(user)

        if not success:
            return Response(
                {"error": msg},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": msg},
            status=status.HTTP_200_OK
        )