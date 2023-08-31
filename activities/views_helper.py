import datetime
from .forms import GarminDataForm
from .models import GarminData


def get_dates_without_garmin_data(
    input_form: GarminDataForm, garmin_data: GarminData
) -> list[datetime.date]:
    """
    function to select input dates that are currently
    not in the database
    """
    return []
