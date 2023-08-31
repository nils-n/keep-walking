from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import GarminData
from .forms import GarminDataForm
from .views_helper import get_dates_without_garmin_data


def view_activities(request):
    """this view loads all activities for the currently logged in user
    it also handles the Form to request data from Garmin
    """

    if request.method == "GET":
        garmin_data = GarminData.objects.filter(user=request.user)
        garmin_form = GarminDataForm()
        context = {"garmin_data": garmin_data, "garmin_form": garmin_form}

    if request.method == "POST":
        garmin_form = GarminDataForm(request.POST)
        garmin_data = GarminData.objects.filter(user=request.user)
        if garmin_form.is_valid():
            form_data = garmin_form.cleaned_data
            start_date = form_data["start_date"]
            end_date = form_data["end_date"]
            new_dates = get_dates_without_garmin_data(start_date, end_date)
            for new_date in new_dates:
                new_garmin_entry = GarminData()
                new_garmin_entry.user = request.user
                new_garmin_entry.date = form_data["start_date"]
                # dummy values - these will be taken from API later
                new_garmin_entry.steps = 6500
                new_garmin_entry.weight_kg = 75
                new_garmin_entry.save()

            return HttpResponseRedirect("/activities/")

    return render(request, "activities_list.html", context)
