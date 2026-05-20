from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers.request.login_serializer import LoginRequestSerializer
from apps.users.schemas.auth.login_schema import login_schema


class LoginAPIView(APIView):

    # =====================================================
    # LOGIN
    # =====================================================
    @login_schema
    def post(self, request):

        serializer = LoginRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].lower().strip()
        password = serializer.validated_data["password"]

        # -------------------------------------------------
        # AUTHENTICATE USER
        # -------------------------------------------------
        user = authenticate(
            request,
            email=email,
            password=password
        )

        if not user:

            return Response(
                {
                    "error": "Invalid email or password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # ACCOUNT STATUS CHECK
        # -------------------------------------------------
        if not user.is_active:

            return Response(
                {
                    "error": "Account is inactive"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------------------------------
        # EMAIL VERIFICATION CHECK
        # -------------------------------------------------
        if not user.email_verified and user.role != "admin":

            return Response(
                {
                    "error": "Email not verified"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------------------------------
        # JWT GENERATION
        # -------------------------------------------------
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "email_verified": user.email_verified,
                }
            },
            status=status.HTTP_200_OK
        )