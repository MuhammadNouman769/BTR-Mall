import random

from django.core.cache import cache

from apps.users.common.services.email_service import send_otp_email


class OTPService:

    OTP_TIMEOUT = 300
    RESEND_TIMEOUT = 60
    MAX_ATTEMPTS = 5

    # =====================================================
    # CACHE KEYS
    # =====================================================

    @staticmethod
    def otp_key(email):
        return f"auth:otp:{email}"

    @staticmethod
    def attempt_key(email):
        return f"auth:otp:attempts:{email}"

    @staticmethod
    def resend_key(email):
        return f"auth:otp:resend:{email}"

    # =====================================================
    # GENERATE OTP
    # =====================================================

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    # =====================================================
    # SEND OTP
    # =====================================================

    @staticmethod
    def send_otp(user):

        email = user.email.lower().strip()

        # -----------------------------------------
        # RESEND PROTECTION
        # -----------------------------------------
        if cache.get(OTPService.resend_key(email)):

            remaining = cache.ttl(
                OTPService.resend_key(email)
            )

            return False, (
                f"Please wait {remaining} seconds before requesting another OTP"
            )

        # -----------------------------------------
        # GENERATE OTP
        # -----------------------------------------
        otp = OTPService.generate_otp()

        # -----------------------------------------
        # SEND EMAIL
        # -----------------------------------------
        success, message = send_otp_email(
            email=email,
            otp=otp
        )

        if not success:
            return False, message

        # -----------------------------------------
        # SAVE OTP
        # -----------------------------------------
        cache.set(
            OTPService.otp_key(email),
            otp,
            timeout=OTPService.OTP_TIMEOUT
        )

        # -----------------------------------------
        # RESET ATTEMPTS
        # -----------------------------------------
        cache.set(
            OTPService.attempt_key(email),
            0,
            timeout=OTPService.OTP_TIMEOUT
        )

        # -----------------------------------------
        # RESEND LOCK
        # -----------------------------------------
        cache.set(
            OTPService.resend_key(email),
            True,
            timeout=OTPService.RESEND_TIMEOUT
        )

        return True, "OTP sent successfully"

    # =====================================================
    # VERIFY OTP
    # =====================================================

    @staticmethod
    def verify_otp(user, code):

        email = user.email.lower().strip()

        otp = cache.get(
            OTPService.otp_key(email)
        )

        attempts = cache.get(
            OTPService.attempt_key(email),
            0
        )

        # -----------------------------------------
        # OTP EXPIRED
        # -----------------------------------------
        if not otp:
            return False, "OTP expired"

        # -----------------------------------------
        # TOO MANY ATTEMPTS
        # -----------------------------------------
        if attempts >= OTPService.MAX_ATTEMPTS:

            cache.delete(
                OTPService.otp_key(email)
            )

            cache.delete(
                OTPService.attempt_key(email)
            )

            return False, "Maximum attempts exceeded"

        # -----------------------------------------
        # INVALID OTP
        # -----------------------------------------
        if str(otp) != str(code):

            cache.set(
                OTPService.attempt_key(email),
                attempts + 1,
                timeout=OTPService.OTP_TIMEOUT
            )

            remaining_attempts = (
                OTPService.MAX_ATTEMPTS - (attempts + 1)
            )

            return False, (
                f"Invalid OTP. {remaining_attempts} attempts remaining"
            )

        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------
        cache.delete(
            OTPService.otp_key(email)
        )

        cache.delete(
            OTPService.attempt_key(email)
        )

        cache.delete(
            OTPService.resend_key(email)
        )

        return True, "OTP verified successfully"