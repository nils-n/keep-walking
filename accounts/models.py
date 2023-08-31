from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    password = models.CharField(max_length=200, blank=True, null=True)
    height_cm = models.IntegerField(null=True)
    birthday = models.DateField(null=True)
    step_goal = models.IntegerField(default=7000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
