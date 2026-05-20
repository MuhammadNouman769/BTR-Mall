from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.choices.status_choices import UserStatusChoices

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "password",
            "confirm_password",
            "role",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 6,
            }
        }

    # =====================================================
    # VALIDATE INPUT
    # =====================================================
    def validate(self, attrs):

        email = attrs.get("email", "").lower().strip()
        phone = attrs.get("phone")

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        # -----------------------------
        # PASSWORD MATCH CHECK
        # -----------------------------
        if password != confirm_password:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })

        # -----------------------------
        # UNIQUE EMAIL CHECK
        # -----------------------------
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "Email already exists"
            })

        # -----------------------------
        # UNIQUE PHONE CHECK
        # -----------------------------
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({
                "phone": "Phone already exists"
            })

        attrs["email"] = email

        return attrs

    # =====================================================
    # CREATE USER
    # =====================================================
    def create(self, validated_data):

        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        # ---------------------------------
        # DEFAULT SYSTEM STATES
        # ---------------------------------
        user.email_verified = False
        user.account_status = UserStatusChoices.PENDING
        user.is_active = False

        user.save()

        return user