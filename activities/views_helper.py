import datetime
import pandas as pd

from .forms import GarminDataForm
from .models import GarminData


def new_dates_for_db(
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[datetime.date]:
    """
    function to select input dates that are currently
    not in the database
    """

    if start_date > end_date:
        return []
    else:
        time_diff = pd.date_range(start=start_date, end=end_date)
        return [date for date in time_diff]
