from django.conf import settings
from django.db import models


class GarminData(models.Model):
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

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.user.username


class Emotion(models.Model):
    class EmotionRating(models.TextChoices):
        BAD = "0", "BAD"
        NEUTRAL = "1", "NEUTRAL"
        GOOD = "2", "GOOD"
        UNDEFINED = "3", "UNDEFINED"

    activity = models.ForeignKey(
        GarminData, on_delete=models.CASCADE, related_name="emotion_rating"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emotion_rating",
    )
    rating = models.IntegerField(
        choices=EmotionRating.choices, default=EmotionRating.UNDEFINED
    )
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
