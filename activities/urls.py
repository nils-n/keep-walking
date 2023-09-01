from django.urls import path

from .views import view_activities, delete_activity

urlpatterns = [
    path("", view_activities, name="view_activities"),
    path(
        "activities/delete_activity/<int:garmin_data_id>/",
        delete_activity,
        name="delete_activity",
    ),
]
