from django.shortcuts import render, redirect
from .models import GarminData


def view_activities(request):
    """this view loads all activities for the currently logged in user"""
    garmin_data = GarminData.objects.all()
    context = {"garmin_data": garmin_data}

    return render(request, "activities_list.html", context)
