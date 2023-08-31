from django.conf import settings
from django.db import models


class GarminData(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    steps = models.PositiveIntegerField(null=True)
    date = models.DateField(null=True)
    weight_kg = models.PositiveIntegerField(null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.user.username
