from django.urls import path

from .views import ActivitiesView

urlpatterns = [
    path("", ActivitiesView.as_view(), name="activities"),
]
