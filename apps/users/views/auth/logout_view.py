from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.schemas.auth.logout_schema import logout_schema


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # LOGOUT USER
    # =====================================================
    @logout_schema
    def post(self, request):

        refresh_token = request.data.get("refresh")

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------
        if not refresh_token:

            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # -------------------------------------------------
            # BLACKLIST TOKEN
            # -------------------------------------------------
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "message": "Logged out successfully"
                },
                status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError:

            return Response(
                {
                    "error": "Token is invalid or already blacklisted"
                },
                status=status.HTTP_400_BAD_REQUEST
            )