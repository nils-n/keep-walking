from django.urls import path

from .views import (
    delete_activity,
    edit_activity,
    load_activities,
    ActivityList,
    rate_good,
    rate_neutral,
    rate_bad,
)

urlpatterns = [
    path("", ActivityList.as_view(), name="activity_home"),
    path("list/", ActivityList.as_view(), name="activity_list"),
    path(
        "list/edit_activity/<int:garmin_data_id>",
        edit_activity,
        name="edit_activity",
    ),
    path(
        "edit_activity/<int:garmin_data_id>",
        edit_activity,
        name="edit_activity",
    ),
]

htmx_urlpatterns = [
    path("load_activities", load_activities, name="load_activities"),
    path(
        "delete_activity/<int:garmin_data_id>/",
        delete_activity,
        name="delete_activity",
    ),
    path("rate_good/<int:garmin_data_id>/", rate_good, name="rate_good"),
    path(
        "rate_neutral/<int:garmin_data_id>/", rate_neutral, name="rate_neutral"
    ),
    path("rate_bad/<int:garmin_data_id>/", rate_bad, name="rate_bad"),
]

urlpatterns += htmx_urlpatterns
