from django.db import models

class SellerTrustLevel(models.TextChoices):
    NEW = "new", "New"
    VERIFIED = "verified", "Verified"
    TRUSTED = "trusted", "Trusted"