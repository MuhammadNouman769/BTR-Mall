from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction

from apps.users.serializers.request.signup_serializer import UserSignupSerializer
from apps.users.services.auth_service import AuthService
from apps.users.services.otp_service import OTPService
from apps.users.schemas import signup_schema


class SignupAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    @signup_schema
    @transaction.atomic
    def post(self, request):

        # -----------------------------------------
        # VALIDATE INPUT
        # -----------------------------------------
        serializer = UserSignupSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        # -----------------------------------------
        # CREATE USER (SERVICE LAYER)
        # -----------------------------------------
        user = AuthService.create_user(serializer)

        # -----------------------------------------
        # SEND OTP
        # -----------------------------------------
        success, msg = OTPService.send_otp(user)

        if not success:
            return Response(
                {
                    "message": "User created but OTP failed",
                    "email": user.email,
                    "otp_sent": False,
                    "error": msg,
                },
                status=status.HTTP_201_CREATED
            )

        # -----------------------------------------
        # SUCCESS RESPONSE
        # -----------------------------------------
        return Response(
            {
                "message": "User registered successfully",
                "email": user.email,
                "otp_sent": True,
                "otp_status": msg,
            },
            status=status.HTTP_201_CREATED
        )