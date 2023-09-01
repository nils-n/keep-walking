import datetime
from datetime import datetime
import pandas as pd

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


def create_date_range(
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[datetime.date]:
    """
    function to create a list of dates in between
    a start and end date
    """

    if start_date > end_date:
        return []
    else:
        # https://www.geeksforgeeks.org/python-iterating-through-a-range-of-dates/
        time_diff = pd.date_range(start=start_date, end=end_date)
        return [date.date() for date in time_diff]


def init_api(email, password):
    api = Garmin(email, password)
    api.login()
    return api


def garmin_api_call(
    garmin_username: str,
    garmin_password: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[str]:
    """calls the data from the garmin api"""
    print("Entering garmin_api_call")
    print(f"  garmin_username {garmin_username} ")
    print(f"  start_date {start_date} ")
    print(f"  end_date {end_date} ")
    try:
        api = init_api(garmin_username, garmin_password)
        output = (
            api.get_daily_steps(start_date.isoformat(), end_date.isoformat()),
        )
        print(output[0])
        print(type(output[0]))
        # example output
        #  ([{'calendarDate': '2023-08-31', 'totalSteps': 1194, 'totalDistance': 945, 'stepGoal': 7000}, {'calendarDate': '2023-09-01', 'totalSteps': 261, 'totalDistance': 207, 'stepGoal': 7000}],)
        return output[0]
    except Exception:
        print("too many API calls ")

    return []


def convert_api_data_to_datetime(garmin_api_data):
    """
    converts the output of the api call into datetime objects
    reason for this function is to make the logic behind the view testable
    """
    return datetime.strptime(
        garmin_api_data["calendarDate"], "%Y-%m-%d"
    ).date()
