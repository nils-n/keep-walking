from django.utils.timezone import now
from django import forms

from .models import GarminData, UserProfile


# to make datepicker work with crispyforms
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
class DateInput(forms.DateInput):
    input_type = "date"


class UserProfileForm(forms.Form):
    birthday = forms.DateField(
        label="Birthday",
        widget=DateInput(
            attrs={
                "id": "user-birthday",
                "required": True,
                "value": now().date(),
                "label": "birthday",
            }
        ),
    )
    height_cm = forms.IntegerField(label=("Height (cm)"))
    step_goal = forms.IntegerField(label="Daily Step Goal")
    start_date = forms.DateField(
        widget=DateInput(
            attrs={
                "id": "user-start-state",
                "required": True,
                "value": now().date(),
                "label": "start_date",
            }
        ),
    )


# setting default TimeDate value for Datepicker from :
# https://stackoverflow.com/questions/55439368/how-to-get-timezone-today-as-default-value
class GarminDataForm(forms.Form):
    start_date = forms.DateField(
        label="Date",
        widget=DateInput(
            attrs={
                "id": "start-date-input",
                "required": True,
                "value": now().date(),
            }
        ),
    )
    garmin_username = forms.CharField(max_length=80, label="Garmin Username")
    garmin_password = forms.CharField(
        max_length=80, label="Garmin Password", widget=forms.PasswordInput()
    )


class EditGarminDataForm(forms.ModelForm):
    class Meta:
        model = GarminData
        fields = ["steps", "weight_kg"]
        widgets = {
            "steps": forms.NumberInput(
                attrs={
                    "id": "edit-steps-input",
                    "required": True,
                    "placeholder": "Number of steps",
                }
            ),
            "weight_kg": forms.NumberInput(
                attrs={
                    "id": "edit-weight-input",
                    "required": True,
                    "placeholder": "Weight in kg",
                }
            ),
        }


class ManualGarminDataForm(forms.ModelForm):
    """
    Form to enter GarminData manually
    """

    class Meta:
        model = GarminData
        fields = ["date", "steps", "weight_kg"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "id": "manually-enter-date",
                    "required": True,
                    "value": now().date(),
                }
            ),
            "steps": forms.NumberInput(
                attrs={
                    "id": "manually-enter-steps",
                    "required": True,
                    "placeholder": "Number of steps",
                }
            ),
            "weight_kg": forms.NumberInput(
                attrs={
                    "id": "manually-enter-weight",
                    "required": True,
                    "placeholder": "Weight in kg",
                }
            ),
        }
