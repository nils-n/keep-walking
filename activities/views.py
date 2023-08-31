import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import GarminData
from .forms import GarminDataForm
from .views_helper import create_date_range, remove_duplicates


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
            start_date = form_data["start_date"]
            # end_date = form_data["end_date"]
            # for quick testing, replace it with start date
            end_date = form_data["start_date"] + datetime.timedelta(days=2)
            new_dates = create_date_range(start_date, end_date)
            new_dates = remove_duplicates(new_dates, existing_dates)
            for new_date in new_dates:
                new_garmin_entry = GarminData()
                new_garmin_entry.user = request.user
                new_garmin_entry.date = new_date
                # dummy values - these will be taken from API later
                new_garmin_entry.steps = 6500
                new_garmin_entry.weight_kg = 75
                new_garmin_entry.save()

            return HttpResponseRedirect("/activities/")

    return render(request, "activities_list.html", context)
