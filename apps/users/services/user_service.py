from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class UserService:

    @staticmethod
    def get_user_by_email(email):

        try:
            return User.objects.get(email=email)

        except ObjectDoesNotExist:
            return None

    @staticmethod
    def user_exists(email):

        return User.objects.filter(
            email=email
        ).exists()

    @staticmethod
    def update_last_login_ip(user, ip):

        user.last_login_ip = ip

        user.save(update_fields=["last_login_ip"])