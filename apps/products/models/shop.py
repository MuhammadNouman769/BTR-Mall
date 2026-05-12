import os
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.text import slugify

from apps.utils.models import SluggedModel
from apps.common.enums import ShopStatusChoices


class Shop(SluggedModel):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shop"
    )

    name = models.CharField(max_length=255)
    handle = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)

    logo = models.ImageField(upload_to="shop/logos/%Y/%m/", null=True, blank=True)
    banner = models.ImageField(upload_to="shop/banners/%Y/%m/", null=True, blank=True)

    cnic_validator = RegexValidator(regex=r'^\d{13}$')
    cnic_number = models.CharField(max_length=13, validators=[cnic_validator], null=True, blank=True)

    cnic_front = models.ImageField(upload_to="shop/cnic/front/%Y/%m/", null=True, blank=True)
    cnic_back = models.ImageField(upload_to="shop/cnic/back/%Y/%m/", null=True, blank=True)
    # shop.py
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    is_trusted_seller = models.BooleanField(default=False)

    shop_status = models.CharField(
        max_length=20,
        choices=ShopStatusChoices.choices,
        default=ShopStatusChoices.PENDING
    )

    rating = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)

    def generate_handle(self):
        base = slugify(self.name)
        slug = base
        counter = 1

        while Shop.objects.filter(handle=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = self.generate_handle()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name