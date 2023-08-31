import datetime
import pandas as pd


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
        return [date for date in time_diff]


def remove_duplicates(
    range_of_dates: list[datetime.date],
    already_existing_dates: list[datetime.date],
) -> list[datetime.date]:
    """
    function to reduce a range of dates to dates that are currrently
    not in the database (to avoid duplicate DB entries)
    """
    return [
        date for date in range_of_dates if date not in already_existing_dates
    ]
