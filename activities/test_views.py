import pytest
import datetime
import pandas as pd
from .views_helper import (
    create_date_range,
    convert_api_data_to_datetime,
    convert_api_data_to_steps,
    extract_weight,
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


# output_weight = (
#     {
#         "startDate": "2023-08-25",
#         "endDate": "2023-09-01",
#         "dateWeightList": [
#             {
#                 "samplePk": 1693438985313,
#                 "date": 1693442578001,
#                 "calendarDate": "2023-08-31",
#                 "weight": 77199.0,
#                 "bmi": None,
#                 "bodyFat": None,
#                 "bodyWater": None,
#                 "boneMass": None,
#                 "muscleMass": None,
#                 "physiqueRating": None,
#                 "visceralFat": None,
#                 "metabolicAge": None,
#                 "sourceType": "MANUAL",
#                 "timestampGMT": 1693438978001,
#                 "weightDelta": None,
#             },
#             {
#                 "samplePk": 1693338330726,
#                 "date": 1693341923002,
#                 "calendarDate": "2023-08-29",
#                 "weight": 78500.0,
#                 "bmi": None,
#                 "bodyFat": None,
#                 "bodyWater": None,
#                 "boneMass": None,
#                 "muscleMass": None,
#                 "physiqueRating": None,
#                 "visceralFat": None,
#                 "metabolicAge": None,
#                 "sourceType": "MANUAL",
#                 "timestampGMT": 1693338323002,
#                 "weightDelta": None,
#             },
#             {
#                 "samplePk": 1693254851757,
#                 "date": 1693258445002,
#                 "calendarDate": "2023-08-28",
#                 "weight": 77400.0,
#                 "bmi": None,
#                 "bodyFat": None,
#                 "bodyWater": None,
#                 "boneMass": None,
#                 "muscleMass": None,
#                 "physiqueRating": None,
#                 "visceralFat": None,
#                 "metabolicAge": None,
#                 "sourceType": "MANUAL",
#                 "timestampGMT": 1693254845002,
#                 "weightDelta": None,
#             },
#             {
#                 "samplePk": 1693152069834,
#                 "date": 1693155664001,
#                 "calendarDate": "2023-08-27",
#                 "weight": 77699.0,
#                 "bmi": None,
#                 "bodyFat": None,
#                 "bodyWater": None,
#                 "boneMass": None,
#                 "muscleMass": None,
#                 "physiqueRating": None,
#                 "visceralFat": None,
#                 "metabolicAge": None,
#                 "sourceType": "MANUAL",
#                 "timestampGMT": 1693152064001,
#                 "weightDelta": None,
#             },
#             {
#                 "samplePk": 1693036193597,
#                 "date": 1693039786007,
#                 "calendarDate": "2023-08-26",
#                 "weight": 77599.0,
#                 "bmi": None,
#                 "bodyFat": None,
#                 "bodyWater": None,
#                 "boneMass": None,
#                 "muscleMass": None,
#                 "physiqueRating": None,
#                 "visceralFat": None,
#                 "metabolicAge": None,
#                 "sourceType": "MANUAL",
#                 "timestampGMT": 1693036186007,
#                 "weightDelta": None,
#             },
#         ],
#         "totalAverage": {
#             "from": 1692921600000,
#             "until": 1693612799999,
#             "weight": 77679.4,
#             "bmi": None,
#             "bodyFat": None,
#             "bodyWater": None,
#             "boneMass": None,
#             "muscleMass": None,
#             "physiqueRating": None,
#             "visceralFat": None,
#             "metabolicAge": None,
#         },
#     },
# )
