from django.contrib import admin
from .models import GarminData, UserProfile, UserAverage


@admin.register(GarminData)
class GarminDataAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "steps",
        "weight_kg",
        "created_at",
        "updated_at",
    )


@admin.register(UserAverage)
class UserAverageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "avg_weight",
        "avg_bmi",
        "avg_bmi_change",
        "bmi_in_healthy_range",
        "bmi_improving_or_maintaining",
        "created_at",
        "updated_at",
    )


admin.site.register(UserProfile)
