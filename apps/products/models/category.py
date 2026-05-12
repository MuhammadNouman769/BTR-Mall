from django.db import models
from django.core.exceptions import ValidationError

from apps.utils.models import OrderedModel, SluggedModel


""" ============================== CATEGORY MODEL ============================ """

class Category(OrderedModel, SluggedModel):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="categories/%Y/%m/", null=True, blank=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["position", "name"]

    def clean(self):
        if self.parent == self:
            raise ValidationError("Category cannot be parent of itself")

        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError("Circular category structure detected")
            parent = parent.parent

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_path(self):
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))

    def __str__(self):
        return self.name