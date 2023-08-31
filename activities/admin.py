from django.contrib import admin
from .models import GarminData


@admin.register(GarminData)
class GarminDataAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "steps",
        "weight_kg",
        "created_at",
        "updated_at",
    )
