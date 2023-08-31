from django.views.generic import ListView
from .models import GarminData


class ActivitiesView(ListView):
    model = GarminData
    template_name = "activities_list.html"
