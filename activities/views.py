from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.timezone import datetime

from .models import GarminData
from .forms import GarminDataForm
from .views_helper import (
    garmin_api_call,
    convert_api_data_to_datetime,
    convert_api_data_to_steps,
)


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
        existing_dates = [db_record.date for db_record in garmin_data]
        if garmin_form.is_valid():
            form_data = garmin_form.cleaned_data
            start_date = form_data["start_date"] - timedelta(days=10)
            end_date = form_data["start_date"]
            garmin_api_data = garmin_api_call(
                form_data["garmin_username"],
                form_data["garmin_password"],
                start_date,
                end_date,
            )
            # extract the dates from the garmin api call
            print(f"--> garmin_api_data : {garmin_api_data}")
            for garmin_entry in garmin_api_data:
                new_date = convert_api_data_to_datetime(garmin_entry)
                new_steps = convert_api_data_to_steps(garmin_entry)
                if new_date not in existing_dates:
                    new_garmin_entry = GarminData()
                    new_garmin_entry.user = request.user
                    new_garmin_entry.date = new_date
                    new_garmin_entry.steps = new_steps
                    new_garmin_entry.weight_kg = 75
                    new_garmin_entry.save()

            return HttpResponseRedirect("/activities/")

    return render(request, "activities_list.html", context)
