from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models.users import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    # =========================================================
    # LIST VIEW
    # =========================================================
    list_display = (
        "id",
        "email",
        "phone",
        "role",
        "account_status",
        "email_verified",
        "phone_verified",
        "is_active",
        "is_staff",
        "created_at",
    )

    list_filter = (
        "role",
        "account_status",
        "is_active",
        "is_staff",
        "email_verified",
        "phone_verified",
        "created_at",
    )

    search_fields = (
        "email",
        "phone",
        "first_name",
        "last_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "last_login",
        "last_login_ip",
        "created_at",
        "updated_at",
    )

    # =========================================================
    # DETAIL PAGE
    # =========================================================
    fieldsets = (

        # -----------------------------------------------------
        # LOGIN INFO
        # -----------------------------------------------------
        (
            "Authentication",
            {
                "fields": (
                    "email",
                    "phone",
                    "password",
                )
            }
        ),

        # -----------------------------------------------------
        # PERSONAL INFO
        # -----------------------------------------------------
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "profile_picture",
                )
            }
        ),

        # -----------------------------------------------------
        # VERIFICATION
        # -----------------------------------------------------
        (
            "Verification",
            {
                "fields": (
                    "email_verified",
                    "phone_verified",
                )
            }
        ),

        # -----------------------------------------------------
        # ROLE & STATUS
        # -----------------------------------------------------
        (
            "Role & Account Status",
            {
                "fields": (
                    "role",
                    "account_status",
                )
            }
        ),

        # -----------------------------------------------------
        # PERMISSIONS
        # -----------------------------------------------------
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),

        # -----------------------------------------------------
        # SYSTEM INFO
        # -----------------------------------------------------
        (
            "System Information",
            {
                "fields": (
                    "last_login",
                    "last_login_ip",
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )

    # =========================================================
    # CREATE USER PAGE
    # =========================================================
    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "role",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    # =========================================================
    # PAGINATION
    # =========================================================
    list_per_page = 25