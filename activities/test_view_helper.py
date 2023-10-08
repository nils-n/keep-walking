import pytest
import datetime
import pandas as pd
from datetime import date
from django.contrib.messages.storage.fallback import FallbackStorage

from .views_helper import (
    create_date_range,
    convert_api_data_to_datetime,
    convert_api_data_to_steps,
    extract_weight,
    convert_date_str_to_datetime,
    calculate_bmi_change,
    extract_user_data,
    extract_bmi_timeseries,
    calculate_average_weight,
    calculate_average_rating,
    calculate_user_stats,
)


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
        (
            {
                "calendarDate": "2023-10-03",
                "stepGoal": 7000,
                "totalDistance": None,
                "totalSteps": None,
            },
            0,
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


@pytest.mark.parametrize(
    "days, avg_bmi, change_bmi, expected_bmi_timeseries",
    [
        (
            [
                datetime.date(2023, 8, 31),
                datetime.date(2023, 8, 30),
                datetime.date(2023, 8, 29),
            ],
            20,
            1,
            [19, 20, 21],
        ),
        (
            [
                datetime.date(2023, 8, 31),
                datetime.date(2023, 8, 30),
                datetime.date(2023, 8, 30),
            ],
            42,
            2,
            [40, 42, 44],
        ),
    ],
)
def test_bmi_timeseries_is_extracted_correctly(
    days, avg_bmi, change_bmi, expected_bmi_timeseries
):
    """
    this test confirms that the BMI timeseries for the bokeh plot
    has correct values
    """
    result = extract_bmi_timeseries(days, avg_bmi, change_bmi)

    assert result == expected_bmi_timeseries


@pytest.mark.parametrize(
    "weight_entries, expected_average",
    [
        ([41, 42, 43], 42),
        ([41, 0, 43], 42),
        ([0, 0, 1], 1),
    ],
)
def test_average_weight_calculated_correctly(
    weight_entries: list[int], expected_average: float
):
    """
    tests that the average weight is calculated correctly
    empty values should be ignored to not affect the average
    """

    result = calculate_average_weight(weight_entries)

    assert result == expected_average


@pytest.mark.parametrize(
    "rating_entries, expected_average_rating",
    [
        ([0, 1, 2], "neutral"),
        ([0, 0, 1], "bad"),
        ([1, 2, 2], "good"),
        ([3, 3, 1], "good"),
    ],
)
def test_average_emotion_rating_calculated_correctly(
    rating_entries: list[int], expected_average_rating: float
):
    """
    tests that the average rating is calculated correctly
    """

    result = calculate_average_rating(rating_entries)

    assert result == expected_average_rating


def test_user_data_extracted_correctly(garmin_data_list):
    """
    this tests the view function that extracts data
    from the DB
    """
    model = garmin_data_list

    days, steps, weights, _ = extract_user_data(model)

    for i, result in enumerate(model):
        assert result.date == days[i].date()
        assert result.weight_kg == weights[i]
        assert result.steps == steps[i]


def test_user_stats_are_calculated_correctly(garmin_data_list):
    """
    this test ensures that the average values are calculated
    correctly from a list of GarminData
    """
    expected_weight = 79.5
    expected_bmi = 26.0
    expected_bmi_change = -2.9
    expectation_whether_BMI_is_in_healthy_range = False
    expectation_whether_BMI_is_improving = True
    random_height_cm = 175

    model = calculate_user_stats(garmin_data_list, random_height_cm)

    assert model[0] == expected_weight
    assert model[1] == expected_bmi
    assert model[2] == expected_bmi_change
    assert model[3] == expectation_whether_BMI_is_in_healthy_range
    assert model[4] == expectation_whether_BMI_is_improving
