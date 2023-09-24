import pytest
import datetime
import pandas as pd
from .models import GarminData
from pandas import to_datetime

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
    model = garmin_data_list

    days, steps, weights = extract_user_data(model)

    for i, result in enumerate(model):
        assert result.date == days[i].date()
        assert result.weight_kg == weights[i]
        assert result.steps == steps[i]


def test_authenticated_user_can_access_profile_page(client, django_user_model):
    """
    this tests whether a signed in user can access their profile page
    """
    username = "testuser2"
    password = "1234-abcd"
    user = django_user_model.objects.create_user(
        username=username, password=password
    )
    client.login(username=username, password=password)
    response = client.get("/activities/profile/1")
    assert response.status_code == 200


def test_unauthenticated_user_cannot_access_profile_page(
    client, django_user_model
):
    """
    this tests whether a 403 error is raised when an unauthorized user
    tries to access a profile page
    """
    response = client.get("/activities/profile/1")
    assert response.status_code == 403


@pytest.mark.parametrize(
    "fixture_name, input_url, expected_status_code",
    [
        ("client", "/activities/wrong-url-1", 404),
        ("client", "/activities/wrong-url-2", 404),
        ("client", "/", 200),
    ],
)
def test_404_is_raised_when_providing_wrong_url(
    fixture_name, input_url, expected_status_code, request
):
    """
    this tests whether a 404 error is raised when the website user
    types in a wrong URL
    """
    client = request.getfixturevalue(fixture_name)

    response = client.get(input_url)

    assert response.status_code == expected_status_code


def test_unauthenticated_user_can_access_home_page(client, django_user_model):
    """
    this tests whether the homepage is display when a not authenticated
    website user visits the page
    """
    response = client.get("/")
    assert response.status_code == 200
