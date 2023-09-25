from datetime import timedelta
import os
from typing import Any, Dict
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.timezone import datetime
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from .models import GarminData, UserProfile
from .forms import GarminDataForm, EditGarminDataForm, UserProfileForm
from .views_helper import (
    garmin_api_call,
    convert_api_data_to_datetime,
    convert_api_data_to_steps,
    extract_weight,
    convert_date_str_to_datetime,
    extract_user_data,
    create_bokeh_plot,
    calculate_bmi_change,
    calculate_bmi_change,
    extract_bmi_timeseries,
)


def user_profile(request, user_id, *args, **kwargs):
    """
    view to see and edit data stored for an
    authenticated user
    """
    if request.user.id == user_id:
        profile = get_object_or_404(UserProfile, user_id=request.user.id)
        profile_form = UserProfileForm()
        context = {"profile_form": profile_form, "user_profile": profile}
        if request.method == "GET":
            return render(request, "profile.html", context)
        elif request.method == "PUT":
            data = QueryDict(request.body).dict()
            profile_form = UserProfileForm(data)
            if profile_form.is_valid():
                form_data = profile_form.cleaned_data
                profile.height_cm = form_data["height_cm"]
                profile.birthday = form_data["birthday"]
                profile.step_goal = form_data["step_goal"]
                profile.start_date = form_data["start_date"]
                profile.save()
                messages.add_message(
                    request, messages.SUCCESS, "Profile edited"
                )
                context = {
                    "profile_form": profile_form,
                    "user_profile": profile,
                }
                return render(
                    request, "partials/profile_details.html", context
                )

    else:
        profile = UserProfile()
        profile_form = UserProfileForm()
        context = {"profile_form": profile_form, "user_profile": profile}
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )
        raise PermissionDenied


def edit_profile(request, user_id, *args, **kwargs):
    """
    view to edit profile of an authenticated user
    https://stackoverflow.com/questions/813418/django-set-field-value-after-a-form-is-initialized
    """
    if request.user.id == user_id:
        profile = get_object_or_404(UserProfile, user_id=request.user.id)
        profile_form = UserProfileForm(
            initial={
                "birthday": profile.birthday,
                "step_goal": profile.step_goal,
                "height_cm": profile.height_cm,
                "start_date": profile.start_date,
            }
        )
        context = {"profile_form": profile_form, "user_profile": profile}
    else:
        raise PermissionDenied
    return render(request, "partials/edit_profile.html", context)


def delete_profile(request, user_id, *args, **kwargs):
    """this view sends a post request to delete an profile."""

    if request.user.id != user_id:
        print("-->no permission to do that")
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )
        profile = UserProfile()
        context = {"user_profile": profile}
        raise PermissionDenied
    else:
        print("searching for user...")
        profile = get_object_or_404(UserProfile, user=request.user)
        print(profile)
        print(" profile found ...")
        print("need to add dialog to confirm here")
        print("--> Not deleting the user for now")
        profile.user.delete()
        messages.add_message(request, messages.SUCCESS, "User Profile deleted")
        return render(request, "partials/delete_profile.html", {})


def update_profile(request, user_id, *args, **kwargs):
    """
    this view creates a profile view of the user
    """
    print("-->entering update_profile")
    queryset = UserProfile.objects.filter(user=user_id)
    profile = get_object_or_404(queryset)

    if request.user.id == user_id:
        print("--> Profile found in DB ")
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            print("Data in form is valid")
            form_data = profile_form.cleaned_data
            profile.height_cm = form_data["height_cm"]
            profile.birthday = form_data["birthday"]
            profile.step_goal = form_data["step_goal"]
            profile.start_date = form_data["start_date"]
            profile.save()
            messages.add_message(
                request, messages.SUCCESS, "Profile Updates edited"
            )

    else:
        profile = UserProfile()
        profile_form = UserProfileForm(request.POST)
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )
        raise PermissionDenied

    # update the template
    user_profile = UserProfile.objects.filter(user=request.user)
    profile = get_object_or_404(user_profile)
    context = {"profile_form": profile_form, "user_profile": profile}

    return render(request, "partials/profile_details.html", context)


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
        garmin_data = self.model.objects.filter(
            user=self.request.user
        ).order_by("-date")
        paginator = Paginator(
            garmin_data, 8
        )  # Show 8 last activities per page.
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # ensure to plot only data from the last 30 days using field lookup
        # and chaining the filter to the existing query
        # https://stackoverflow.com/questions/1984047/django-filter-older-than-days
        first_day_for_bokeh_plot = datetime.now() - timedelta(days=30)
        garmin_data_bokeh = garmin_data.filter(
            user=self.request.user, date__gte=first_day_for_bokeh_plot
        ).order_by("-date")

        # provide data strucutre for bokeh
        # this will create components for the template
        # https://docs.bokeh.org/en/2.4.3/docs/user_guide/embed.html
        days, steps, weights = extract_user_data(garmin_data_bokeh)

        # create pandas dataframe for tooltips
        # https://stackoverflow.com/questions/48792770/bokeh-hovertool-tooltips-showing-date-as-number
        data = pd.DataFrame()
        data["Date"] = pd.to_datetime(days, format="%Y-%m-%d")
        data["DateString"] = data["Date"].dt.strftime("%Y-%m-%d")
        data.insert(2, "Steps", pd.to_numeric(steps))

        # calculate the average bmi and the linear trend for the last 30 days
        # get height from the user profile for calculating BMI
        user_profile = UserProfile.objects.filter(user=self.request.user)
        profile = get_object_or_404(user_profile)
        average_bmi, change_bmi = calculate_bmi_change(
            days, weights, profile.height_cm
        )
        bmi = extract_bmi_timeseries(days, average_bmi, change_bmi)
        bmi = bmi[::-1]
        print(f"average : {average_bmi}")
        print(f"change_bmi : {change_bmi}")
        print(f"bmi : {bmi}")

        # create a bokeh plot and styling of the plot inside a helper function
        script, div = create_bokeh_plot(data, "Steps")

        # create a second bokeh plot with the BMI progression
        data_bmi = pd.DataFrame()
        data_bmi["Date"] = pd.to_datetime(days, format="%Y-%m-%d")
        data_bmi["DateString"] = data["Date"].dt.strftime("%Y-%m-%d")
        data_bmi.insert(2, "BMI", pd.to_numeric(bmi))
        script_bmi, div_bmi = create_bokeh_plot(data_bmi, "BMI")

        context_data["average_bmi"] = average_bmi
        context_data["change_bmi"] = change_bmi
        context_data["garmin_form"] = GarminDataForm()
        context_data["page_obj"] = page_obj
        context_data["script"] = script
        context_data["div"] = div
        context_data["script_bmi"] = script_bmi
        context_data["div_bmi"] = div_bmi
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

    # it's just for the moment - start and end date are switched. Once the
    # final UI in place, handle the naming conventions better.
    garmin_end_date = convert_date_str_to_datetime(start_date)
    garmin_start_date = garmin_end_date - timedelta(days=25)

    # load information about the currently stored data for the user
    garmin_data = GarminData.objects.filter(user=request.user)
    existing_dates = [db_record.date for db_record in garmin_data]

    # retrieve latest data from garmin api
    garmin_step_data, garmin_weight_data = garmin_api_call(
        garmin_username,
        garmin_password,
        garmin_start_date,
        garmin_end_date,
    )
    messages.add_message(
        request, messages.ERROR, "Sync with Garmin API successful"
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
            new_garmin_entry.save()
    # update the template
    garmin_data = GarminData.objects.filter(user=request.user).order_by(
        "-date"
    )
    paginator = Paginator(garmin_data, 8)  # Show 8 last activities per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "partials/activities.html",
        {
            "garmin_data": garmin_data,
            "page_obj": page_obj,
        },
    )


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
        raise PermissionDenied
    # update the template
    garmin_data = GarminData.objects.filter(user=request.user).order_by(
        "-date"
    )
    paginator = Paginator(garmin_data, 8)  # Show 8 last activities per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "partials/activities.html",
        {
            "garmin_data": garmin_data,
            "page_obj": page_obj,
        },
    )


def edit_activity(request, garmin_data_id, *args, **kwargs):
    """
    this view sends a post request to edit an existing activity
    """
    garmin_data = get_object_or_404(GarminData, id=garmin_data_id)

    if request.method == "POST":
        edit_garmin_form = EditGarminDataForm(request.POST)
        if edit_garmin_form.is_valid():
            form_data = edit_garmin_form.cleaned_data
            garmin_data.steps = form_data["steps"]
            garmin_data.weight_kg = form_data["weight_kg"]
            garmin_data.save()
            messages.add_message(request, messages.SUCCESS, "Entry edited")
        else:
            messages.add_message(request, messages.ERROR, "Could not edit")

        return HttpResponseRedirect("/activities/list")

    else:
        data = {
            "date": garmin_data.date,
            "weight_kg": garmin_data.weight_kg,
            "steps": garmin_data.steps,
        }
        garmin_form = EditGarminDataForm(initial=data)
        context = {"garmin_edit_form": garmin_form, "date": garmin_data.date}
        return render(request, "edit_activity.html", context)


def rate_good(request, garmin_data_id):
    """
    this views sends a POST request of a user rating
    of an activity
    """
    garmin_data = get_object_or_404(GarminData, id=garmin_data_id)

    if garmin_data.user.username == request.user.username:
        if garmin_data.rating == garmin_data.EmotionRating.UNDEFINED:
            print("-->Emotion does not exist : creating now. ")
            garmin_data.rating = garmin_data.EmotionRating.GOOD
            garmin_data.save()
            request, messages.SUCCESS, "Emotion Rating successful"
        else:
            print("-->Emotion exists : updating now. ")
            garmin_data.rating = garmin_data.EmotionRating.GOOD
            garmin_data.save()
            request, messages.SUCCESS, "Emotion Rating changed successfully"
    else:
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )
        raise PermissionDenied
    # update the template
    garmin_data = GarminData.objects.filter(user=request.user).order_by(
        "-date"
    )
    paginator = Paginator(garmin_data, 8)  # Show 8 last activities per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "partials/activities.html",
        {
            "garmin_data": garmin_data,
            "page_obj": page_obj,
        },
    )


def rate_neutral(request, garmin_data_id):
    """
    this views sends a POST request of a neutral user rating
    of an activity
    """
    garmin_data = get_object_or_404(GarminData, id=garmin_data_id)

    if garmin_data.user.username == request.user.username:
        if garmin_data.rating == garmin_data.EmotionRating.UNDEFINED:
            print("-->Emotion does not exist : creating now. ")
            garmin_data.rating = garmin_data.EmotionRating.NEUTRAL
            garmin_data.save()
            request, messages.SUCCESS, "Emotion Rating successful"
        else:
            print("-->Emotion exists : updating now. ")
            garmin_data.rating = garmin_data.EmotionRating.NEUTRAL
            garmin_data.save()
            request, messages.SUCCESS, "Emotion Rating changed successfully"
    else:
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )
        raise PermissionDenied
    # update the template
    garmin_data = GarminData.objects.filter(user=request.user).order_by(
        "-date"
    )
    paginator = Paginator(garmin_data, 8)  # Show 8 last activities per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "partials/activities.html",
        {
            "garmin_data": garmin_data,
            "page_obj": page_obj,
        },
    )


def rate_bad(request, garmin_data_id):
    """
    this views sends a POST request of a bad user rating
    of an activity
    """
    garmin_data = get_object_or_404(GarminData, id=garmin_data_id)

    if garmin_data.user.username == request.user.username:
        if garmin_data.rating == garmin_data.EmotionRating.UNDEFINED:
            print("-->Emotion does not exist : creating now. ")
            garmin_data.rating = garmin_data.EmotionRating.BAD
            garmin_data.save()
            request, messages.SUCCESS, "Emotion Rating successful"
        else:
            print("-->Emotion exists : updating now. ")
            garmin_data.rating = garmin_data.EmotionRating.BAD
            garmin_data.save()
            request, messages.SUCCESS, "Emotion Rating changed successfully"
    else:
        messages.add_message(
            request, messages.ERROR, "No permission to do this request"
        )
        raise PermissionDenied
    # update the template
    garmin_data = GarminData.objects.filter(user=request.user).order_by(
        "-date"
    )
    paginator = Paginator(garmin_data, 8)  # Show 8 last activities per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "partials/activities.html",
        {
            "garmin_data": garmin_data,
            "page_obj": page_obj,
        },
    )
