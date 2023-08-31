from django.urls import path

from .views import view_activities

urlpatterns = [
    path("", view_activities, name="view_activities"),
]
