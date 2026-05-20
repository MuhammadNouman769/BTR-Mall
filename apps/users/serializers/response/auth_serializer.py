from rest_framework import serializers
from .user_serializer import UserSerializer


# =========================================================
# SIGNUP RESPONSE
# =========================================================
class SignupResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    email = serializers.EmailField()


# =========================================================
# LOGIN RESPONSE
# =========================================================
class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


# =========================================================
# GENERIC MESSAGE RESPONSE
# =========================================================
class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


# =========================================================
# ERROR RESPONSE
# =========================================================
class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()


# =========================================================
# LOGOUT RESPONSE
# =========================================================
class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    logged_out_at = serializers.DateTimeField()