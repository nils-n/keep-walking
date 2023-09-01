from django.urls import path

from .views import view_activities, delete_activity, edit_activity

urlpatterns = [
    path("", view_activities, name="view_activities"),
    path(
        "delete_activity/<int:garmin_data_id>/",
        delete_activity,
        name="delete_activity",
    ),
    path(
        "edit_activity/<int:garmin_data_id>",
        edit_activity,
        name="edit_activity",
    ),
]
