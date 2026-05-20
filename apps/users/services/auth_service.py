from django.contrib.auth import get_user_model
from django.db import transaction
from apps.users.common.services.email_service import send_welcome_email
from apps.users.choices.status_choices import UserStatusChoices


User = get_user_model()


class AuthService:

    # =====================================================
    # CREATE USER
    # =====================================================
    @staticmethod
    @transaction.atomic
    def create_user(serializer):

        user = serializer.save()
        
        return user
        
        
        
        

    # =====================================================
    # ACTIVATE USER
    # =====================================================
    @staticmethod
    @transaction.atomic
    def activate_user(user):

        if user.account_status == UserStatusChoices.ACTIVE:
            return user

        user.account_status = UserStatusChoices.ACTIVE
        user.email_verified = True
        user.is_active = True
        
        # Send welcome email
        send_welcome_email(
            email=user.email,
            user_name=user.email.split("@")[0]
        )

        user.save(
            update_fields=[
                "account_status",
                "email_verified",
                "is_active",
            ]
        )

        return user

    # =====================================================
    # SUSPEND USER
    # =====================================================
    @staticmethod
    @transaction.atomic
    def suspend_user(user):

        user.account_status = UserStatusChoices.SUSPENDED
        user.is_active = False

        user.save(
            update_fields=[
                "account_status",
                "is_active",
            ]
        )

        return user

    # =====================================================
    # DEACTIVATE USER
    # =====================================================
    @staticmethod
    @transaction.atomic
    def deactivate_user(user):

        user.account_status = UserStatusChoices.INACTIVE
        user.is_active = False

        user.save(
            update_fields=[
                "account_status",
                "is_active",
            ]
        )

        return user