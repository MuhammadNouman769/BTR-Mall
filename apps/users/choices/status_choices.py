from django.db import models
from django.utils.translation import gettext_lazy as _


class UserStatusChoices(models.TextChoices):

    PENDING = "pending", _("Pending")
    ACTIVE = "active", _("Active")
    SUSPENDED = "suspended", _("Suspended")
    BLOCKED = "blocked", _("Blocked")