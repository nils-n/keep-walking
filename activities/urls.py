from django.urls import path

from .views import view_activities, delete_activity

urlpatterns = [
    path("", view_activities, name="view_activities"),
    path("post/ajax/delete_activity", delete_activity, name="delete_activity"),
]
