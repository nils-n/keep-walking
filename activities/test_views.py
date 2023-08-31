import pytest
import datetime
import pandas as pd
from .views_helper import create_date_range, remove_duplicates


def test_the_obvious():
    assert True == True


@pytest.mark.parametrize(
    "start_date, end_date, expected_output",
    [
        (datetime.date(2023, 8, 31), datetime.date(2023, 8, 15), True),
        (datetime.date(2023, 8, 15), datetime.date(2023, 8, 31), False),
    ],
)
def test_should_return_empty_list_when_start_date_after_end_date(
    start_date, end_date, expected_output
):
    """
    When the start date is after the end date, this function
    should return an empty list
    """
    model = create_date_range(start_date, end_date)

    if not model:
        is_empty = True
    else:
        is_empty = False

    assert is_empty == expected_output


@pytest.mark.parametrize(
    "date_range, range_of_exisiting_db_record, expected_number_of_dates",
    [
        (
            pd.date_range(
                start=datetime.date(2023, 8, 20),
                end=datetime.date(2023, 8, 30),
            ),
            pd.date_range(
                start=datetime.date(2023, 8, 25),
                end=datetime.date(2023, 8, 26),
            ),
            9,
        ),
        (
            pd.date_range(
                start=datetime.date(2023, 8, 20),
                end=datetime.date(2023, 8, 30),
            ),
            pd.date_range(
                start=datetime.date(1900, 8, 18),
                end=datetime.date(1900, 8, 20),
            ),
            11,
        ),
    ],
)
def test_should_remove_all_duplicated_days(
    date_range, range_of_exisiting_db_record, expected_number_of_dates
):
    """
    This test should test whether the function can remove all duplicates
    from the input list
    """
    random_input_range = [date for date in date_range]
    random_range_of_existing_dates = [
        date for date in range_of_exisiting_db_record
    ]

    model = remove_duplicates(
        random_input_range, random_range_of_existing_dates
    )

    assert len(model) == expected_number_of_dates
