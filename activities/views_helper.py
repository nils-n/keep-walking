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
        return [date.date() for date in time_diff]
