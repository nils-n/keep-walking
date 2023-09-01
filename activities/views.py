from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.timezone import datetime

from .models import GarminData
from .forms import GarminDataForm
from .views_helper import (
    create_date_range,
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
        print(f" existing dates  {existing_dates}")
        if garmin_form.is_valid():
            form_data = garmin_form.cleaned_data
            start_date = form_data["start_date"] - timedelta(days=10)
            end_date = form_data["start_date"]
            new_dates = create_date_range(start_date, end_date)
            print("---------------------------------")
            print("--> calling garmin api ")
            garmin_api_data = garmin_api_call(
                form_data["garmin_username"],
                form_data["garmin_password"],
                start_date,
                end_date,
            )
            # garmin_api_data = [
            #     {
            #         "calendarDate": "2023-08-31",
            #         "totalSteps": 1194,
            #         "totalDistance": 945,
            #         "stepGoal": 7000,
            #     },
            #     {
            #         "calendarDate": "2023-09-01",
            #         "totalSteps": 261,
            #         "totalDistance": 207,
            #         "stepGoal": 7000,
            #     },
            # ]
            # [{'calendarDate': '2023-08-22', 'totalSteps': 7385, 'totalDistance': 6288, 'stepGoal': 7000}, {'calendarDate': '2023-08-23', 'totalSteps': 7942, 'totalDistance': 6288, 'stepGoal': 7000}, {'calendarDate': '2023-08-24', 'totalSteps': 2809, 'totalDistance': 2243, 'stepGoal': 7000}, {'calendarDate': '2023-08-25', 'totalSteps': 3625, 'totalDistance': 2870, 'stepGoal': 7000}, {'calendarDate': '2023-08-26', 'totalSteps': 7519, 'totalDistance': 5953, 'stepGoal': 7000}, {'calendarDate': '2023-08-27', 'totalSteps': 14899, 'totalDistance': 11796, 'stepGoal': 7000}, {'calendarDate': '2023-08-28', 'totalSteps': 7147, 'totalDistance': 5667, 'stepGoal': 7000}, {'calendarDate': '2023-08-29', 'totalSteps': 2151, 'totalDistance': 1711, 'stepGoal': 7000}, {'calendarDate': '2023-08-30', 'totalSteps': 3546, 'totalDistance': 2807, 'stepGoal': 7000}, {'calendarDate': '2023-08-31', 'totalSteps': 1194, 'totalDistance': 945, 'stepGoal': 7000}, {'calendarDate': '2023-09-01', 'totalSteps': 261, 'totalDistance': 207, 'stepGoal': 7000}]

            # extract the dates from the garmin api call
            print(f"--> garmin_api_data : {garmin_api_data}")
            print("---------------------------------")
            print(f" new_dates dates  {new_dates}")
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
