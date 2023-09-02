from datetime import timedelta
import os
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.timezone import datetime
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView

from .models import GarminData
from .forms import GarminDataForm, EditGarminDataForm
from .views_helper import (
    garmin_api_call,
    convert_api_data_to_datetime,
    convert_api_data_to_steps,
    extract_weight,
    get_garmin_mock_data_for_testing,
    convert_date_str_to_datetime,
)


class ActivityList(ListView):
    """
    this view loads all activities for the user
    https://stackoverflow.com/questions/36950416/when-to-use-get-get-queryset-get-context-data-in-django
    """

    template_name = "activities_list.html"
    model = GarminData
    context_object_name = "garmin_data"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["garmin_form"] = GarminDataForm()
        return context_data

    def get_queryset(self):
        return GarminData.objects.filter(user=self.request.user)


def load_activities(request):
    """
    this views loads all activities from the Garmin API
    into the DB
    """
    print("-->views.py : entering load_activities")
    garmin_username = request.POST.get("garmin_username")
    garmin_password = request.POST.get("garmin_password")
    start_date = request.POST.get("start_date")
    print(start_date)

    start_date = convert_date_str_to_datetime(start_date)
    end_date = start_date - timedelta(days=10)

    # load information about the currently stored data for the user
    garmin_data = GarminData.objects.filter(user=request.user)
    existing_dates = [db_record.date for db_record in garmin_data]

    # for the moment just fake an API call - will add this once the rest is working
    use_mockdata = True
    print(f"use_mockdata : {use_mockdata}")
    if use_mockdata:
        print("calling with fake API data")
        print(use_mockdata)
        (
            garmin_step_data,
            garmin_weight_data,
        ) = get_garmin_mock_data_for_testing()
    else:
        print("calling the actual Garmin API data")
        garmin_step_data, garmin_weight_data = garmin_api_call(
            garmin_username,
            garmin_password,
            start_date,
            end_date,
        )
    garmin_step_data = garmin_step_data[0]

    for garmin_entry in garmin_step_data:
        new_date = convert_api_data_to_datetime(garmin_entry)
        new_steps = convert_api_data_to_steps(garmin_entry)
        if new_date not in existing_dates:
            new_garmin_entry = GarminData()
            new_garmin_entry.user = request.user
            new_garmin_entry.date = new_date
            new_garmin_entry.steps = new_steps
            new_garmin_entry.weight_kg = extract_weight(
                garmin_weight_data[0], new_date
            )
            print(
                f"weight on date {new_date} was : {new_garmin_entry.weight_kg}"
            )
            new_garmin_entry.save()

    # update the template
    garmin_data = GarminData.objects.filter(user=request.user)
    return render(
        request, "partials/activities.html", {"garmin_data": garmin_data}
    )


# def view_activities(request):
#     """this view loads all activities for the currently logged in user
#     it also handles the Form to request data from Garmin
#     """

#     if request.method == "GET":
#         garmin_data = GarminData.objects.filter(user=request.user)
#         garmin_form = GarminDataForm()
#         context = {"garmin_data": garmin_data, "garmin_form": garmin_form}

#     if request.method == "POST":
#         garmin_form = GarminDataForm(request.POST)
#         garmin_data = GarminData.objects.filter(user=request.user)
#         existing_dates = [db_record.date for db_record in garmin_data]
#         if garmin_form.is_valid():
#             form_data = garmin_form.cleaned_data
#             start_date = form_data["start_date"] - timedelta(days=10)
#             end_date = form_data["start_date"]
#             # just to be on the cautious side to not call the Garmin API too often
#             # (and riksing being blocked by Garmin), i will comment the API call
#             # out for now and replace it mock data. later on, i will activate the
#             # actual api call again
#             use_mockdata = True
#             if use_mockdata:
#                 print("calling with fake API data")
#                 print(use_mockdata)
#                 (
#                     garmin_step_data,
#                     garmin_weight_data,
#                 ) = get_garmin_mock_data_for_testing()
#             else:
#                 print("calling the actual Garmin API data")
#                 garmin_step_data, garmin_weight_data = garmin_api_call(
#                     form_data["garmin_username"],
#                     form_data["garmin_password"],
#                     start_date,
#                     end_date,
#                 )
#             garmin_step_data = garmin_step_data[0]
#             # extract the dates from the garmin api call
#             # print(f"--> garmin_step_data : {garmin_step_data}")
#             # print(f"--> garmin_weight_data : {garmin_weight_data}")
#             for garmin_entry in garmin_step_data:
#                 new_date = convert_api_data_to_datetime(garmin_entry)
#                 new_steps = convert_api_data_to_steps(garmin_entry)
#                 if new_date not in existing_dates:
#                     new_garmin_entry = GarminData()
#                     new_garmin_entry.user = request.user
#                     new_garmin_entry.date = new_date
#                     new_garmin_entry.steps = new_steps
#                     new_garmin_entry.weight_kg = extract_weight(
#                         garmin_weight_data[0], new_date
#                     )
#                     print(
#                         f"weight on date {new_date} was : {new_garmin_entry.weight_kg}"
#                     )
#                     new_garmin_entry.save()

#             return HttpResponseRedirect("/activities/")

#     return render(request, "activities_list.html", context)


def delete_activity(request, garmin_data_id, *args, **kwargs):
    """
    this view sends a post request to delete an activity.
    """
    garmin_data = get_object_or_404(GarminData, id=garmin_data_id)

    if garmin_data.user.username == request.user.username:
        garmin_data.delete()
        messages.add_message(request, messages.SUCCESS, "Entry deleted")
    else:
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )

    return HttpResponseRedirect("/activities/")


def edit_activity(request, garmin_data_id, *args, **kwargs):
    """
    this view sends a post request to edit an existing activity
    """
    garmin_data = get_object_or_404(GarminData, id=garmin_data_id)

    if request.method == "POST":
        edit_garmin_form = EditGarminDataForm(request.POST)
        if edit_garmin_form.is_valid():
            print("halleluja")
            form_data = edit_garmin_form.cleaned_data
            garmin_data.steps = form_data["steps"]
            garmin_data.weight_kg = form_data["weight_kg"]
            garmin_data.save()
            messages.add_message(request, messages.SUCCESS, "Entry edited")
        else:
            messages.add_message(request, messages.ERROR, "Could not edit")

        return HttpResponseRedirect("/activities/")

    else:
        data = {
            "date": garmin_data.date,
            "weight_kg": garmin_data.weight_kg,
            "steps": garmin_data.steps,
        }
        garmin_form = EditGarminDataForm(initial=data)
        context = {"garmin_edit_form": garmin_form, "date": garmin_data.date}
        return render(request, "edit_activity.html", context)
