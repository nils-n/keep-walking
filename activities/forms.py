from django import forms


# to make datepicker work with crispyforms
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
class DateInput(forms.DateInput):
    input_type = "date"


class GarminDataForm(forms.Form):
    start_date = forms.DateField(
        widget=DateInput(
            attrs={
                "id": "start-date-input",
                "required": True,
                "placeholder": "Start Date",
            }
        )
    )
