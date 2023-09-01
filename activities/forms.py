from django.utils.timezone import now
from django import forms


# to make datepicker work with crispyforms
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
class DateInput(forms.DateInput):
    input_type = "date"


# setting default TimeDate value for Datepicker from :
# https://stackoverflow.com/questions/55439368/how-to-get-timezone-today-as-default-value
class GarminDataForm(forms.Form):
    start_date = forms.DateField(
        widget=DateInput(
            attrs={
                "id": "start-date-input",
                "required": True,
                "placeholder": "Start Date",
                "value": now().date(),
            }
        )
    )
