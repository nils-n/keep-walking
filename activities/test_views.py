import pytest
import datetime
import pandas as pd
from .models import GarminData

from .views_helper import (
    create_date_range,
    convert_api_data_to_datetime,
    convert_api_data_to_steps,
    extract_weight,
    convert_date_str_to_datetime,
    calculate_bmi_change,
    extract_user_data,
)


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
    "input_date_from_api, expected_datetime_object",
    [
        (
            {
                "calendarDate": "2023-08-31",
            },
            datetime.date(2023, 8, 31),
        ),
        (
            {
                "calendarDate": "2010-01-01",
            },
            datetime.date(2010, 1, 1),
        ),
    ],
)
def test_converts_api_date_format_correctly_into_djangos_datetime(
    input_date_from_api, expected_datetime_object
):
    """test whether the input string as fetched from the api converts
    correctly into pythons datetime format"""
    model = convert_api_data_to_datetime(input_date_from_api)

    assert model == expected_datetime_object


@pytest.mark.parametrize(
    "input_date_str, expected_datetime_object",
    [
        ("2023-09-02", datetime.date(2023, 9, 2)),
        ("2023-09-03", datetime.date(2023, 9, 3)),
    ],
)
def test_converts_date_str_correctly_to_datetime(
    input_date_str, expected_datetime_object
):
    """
    test to confirm that date strings are converted correctly into
    pythons datetime data structure
    """
    model = convert_date_str_to_datetime(input_date_str)

    assert model == expected_datetime_object


@pytest.mark.parametrize(
    "input_steps_from_api, expected_step_count",
    [
        (
            {
                "totalSteps": "42",
            },
            42,
        ),
        (
            {
                "totalSteps": "1000",
            },
            1000,
        ),
    ],
)
def test_that_step_count_converts_correctly_to_integer(
    input_steps_from_api, expected_step_count
):
    """
    test whether input json from api call converts correctly to
    step count of that day
    """
    model = convert_api_data_to_steps(input_steps_from_api)

    assert model == expected_step_count


@pytest.mark.parametrize(
    "garmin_weight_data, target_date, expected_output",
    [
        (
            {
                "dateWeightList": [
                    {
                        "calendarDate": "2023-08-31",
                        "weight": 77199.0,
                    }
                ],
            },
            datetime.date(2023, 8, 31),
            77,
        ),
        (
            {
                "dateWeightList": [
                    {
                        "calendarDate": "2023-08-31",
                        "weight": 77199.0,
                    }
                ],
            },
            datetime.date(1900, 1, 1),
            0,
        ),
    ],
)
def test_that_weight_data_is_extracted_from_correct_date(
    garmin_weight_data, target_date, expected_output
):
    """
    This test confirms that the weight data is extracted correctly
    from the api call for the body weight
    """

    model = extract_weight(garmin_weight_data, target_date)

    assert model == expected_output


@pytest.mark.parametrize(
    "days, weights, height, expected_avg_bmi, expected_bmi_change",
    [
        (
            [
                datetime.date(2023, 8, 31),
                datetime.date(2023, 8, 30),
                datetime.date(2023, 8, 29),
            ],
            [
                96,
                96,
                96,
            ],
            200,
            24,
            0,
        ),
        (
            [
                datetime.date(2023, 8, 31),
                datetime.date(2023, 8, 30),
            ],
            [
                96,
                128,
            ],
            200,
            28,
            -8,
        ),
    ],
)
def test_bmi_change_is_calculated_correctly(
    days, weights, height, expected_avg_bmi, expected_bmi_change
):
    """
    this test confirms that the helper function calculates the
    avearage BMI and the change of BMI over a given time correctly
    """
    bmi, change_of_bmi = calculate_bmi_change(days, weights, height)

    assert bmi == expected_avg_bmi
    assert change_of_bmi == expected_bmi_change


def test_confirm_that_userdata_factory_works(db, user_factory):
    """
    this tests that we can use the factory for the user
    in our unit tests
    """
    model = user_factory.build()

    result = model.username

    assert isinstance(result, str)


def test_confirm_that_garmin_data_factory_works(db, garmindata_factory):
    """
    this tests that we can use the factory for the GarminData model
    for unit tests of functions that use this model
    """
    model = garmindata_factory.build()

    assert isinstance(model.steps, int)
    assert isinstance(model.weight_kg, int)


def test_user_data_extracted_correctly(garmin_data_list):
    """
    this tests the view function that extracts data
    from the DB
    """
    model, expected_steps, expected_weights, expected_dates = garmin_data_list

    days, steps, weights = extract_user_data(model)

    for i, result in enumerate(model):
        assert result.date == expected_dates[i]
        assert result.weight_kg == expected_weights[i]
        assert result.steps == expected_steps[i]
