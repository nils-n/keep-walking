from django.conf import settings
from django.db import models
from django.db.models.signals import post_save


class GarminData(models.Model):
    """Data Table for imported values from Garmin API"""

    class EmotionRating(models.IntegerChoices):
        """Choices for Emotional Ratings of an Activity"""

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
        """arrange them by latest date first"""

        ordering = ["-date"]

    def __str__(self):
        return settings.user.username


class UserAverage(models.Model):
    """
    Model to describe average user progression on the website
    over past 25 days
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_average",
    )
    avg_weight = models.FloatField()
    avg_bmi = models.FloatField()
    avg_bmi_change = models.FloatField()
    bmi_in_healthy_range = models.BooleanField()
    bmi_improving_or_maintaining = models.BooleanField()
    date = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

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
    height_cm = models.IntegerField(default=170)
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
