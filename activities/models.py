from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class GarminData(models.Model):
    class EmotionRating(models.IntegerChoices):
        BAD = 0
        NEUTRAL = 1
        GOOD = 2
        UNDEFINED = 3

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="garmin_data",
    )
    steps = models.PositiveIntegerField(null=True)
    date = models.DateField(null=True)
    weight_kg = models.PositiveIntegerField(null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    rating = models.IntegerField(
        choices=EmotionRating.choices, default=EmotionRating.UNDEFINED
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(null=True)
    height_cm = models.IntegerField(null=True)
    step_goal = models.IntegerField(default=7000)
    start_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    """
    Use signals to create UserProfile when a new user is created
    Automatically Create User Profiles - Django Wednesdays Twitter #3
    https://www.youtube.com/watch?v=H8MmNqDyra8
    """
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
