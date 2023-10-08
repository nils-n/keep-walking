import pytest
import pandas as pd
from .models import GarminData
from datetime import date
from django.contrib.messages.storage.fallback import FallbackStorage

from .views import delete_activity, load_activities_manually


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
    fixture_name, input_url, expected_status_code, request, db
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


@pytest.mark.parametrize()(
    "client_fixture_name, model_fixture_name, url, expected_status_code",
    [
        (
            "client",
            "django_user_model",
            "/activities/profile/1/edit_profile",
            200,
        ),
        (
            "client",
            "django_user_model",
            "/activities/profile/2/edit_profile",
            403,
        ),
        (
            "client",
            "django_user_model",
            "/activities/profile/1/delete_profile",
            200,
        ),
        (
            "client",
            "django_user_model",
            "/activities/profile/2/delete_profile",
            403,
        ),
        (
            "client",
            "django_user_model",
            "/activities/list/",
            200,
        ),
    ],
)
def test_authenticated_users_can_access_personal_pages(
    client_fixture_name, model_fixture_name, url, expected_status_code, request
):
    """
    this tests whether a signed in user can access their personal area
    """
    client = request.getfixturevalue(client_fixture_name)
    django_user_model = request.getfixturevalue(model_fixture_name)

    username = "testuser2"
    password = "1234-abcd"
    user = django_user_model.objects.create_user(
        username=username, password=password
    )
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == expected_status_code


@pytest.mark.parametrize()(
    "client_fixture_name, model_fixture_name, url, expected_status_code",
    [
        (
            "client",
            "django_user_model",
            "/activities/load_activities_manually",
            200,
        ),
    ],
)
def test_authenticated_users_enter_activities_manually(
    client_fixture_name,
    model_fixture_name,
    url,
    expected_status_code,
    db,
    request,
):
    """
    this tests whether a signed in user can edit their activities
    """
    client = request.getfixturevalue(client_fixture_name)
    django_user_model = request.getfixturevalue(model_fixture_name)

    username = "testuser2"
    password = "1234-abcd"
    user = django_user_model.objects.create_user(
        username=username, password=password
    )
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == expected_status_code


@pytest.mark.parametrize()(
    "client_fixture_name, model_fixture_name, garmin_fixture_name,  url, expected_status_code",
    [
        (
            "client",
            "django_user_model",
            "garmin_data",
            "/activities/list/edit_activity/1",
            200,
        ),
        (
            "client",
            "django_user_model",
            "garmin_data",
            "/activities/list/edit_activity/42",
            404,
        ),
    ],
)
def test_authenticated_users_can_call_view_to_edit_activities(
    client_fixture_name,
    model_fixture_name,
    garmin_fixture_name,
    url,
    expected_status_code,
    request,
):
    """
    this tests whether a signed in user can call view to edit activities
    """
    client = request.getfixturevalue(client_fixture_name)
    django_user_model = request.getfixturevalue(model_fixture_name)

    # arrange : user that has activities stored in DB
    username = "testuser2"
    password = "1234-abcd"
    user = django_user_model.objects.create_user(
        username=username, password=password
    )
    garmin_data = request.getfixturevalue(garmin_fixture_name)
    garmin_data.user = user
    garmin_data.save()

    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == expected_status_code


@pytest.mark.parametrize()(
    "client_fixture_name, model_fixture_name, garmin_fixture_name,  \
    request_fixture, url, expected_status_code",
    [
        (
            "client",
            "django_user_model",
            "garmin_data",
            "rf",
            "/activities/delete_activity/1",
            200,
        ),
    ],
)
def test_authenticated_users_can_enter_view_to_delete_activities(
    client_fixture_name,
    model_fixture_name,
    garmin_fixture_name,
    request_fixture,
    url,
    expected_status_code,
    request,
):
    """
    this tests whether a signed in user can call view to delete
    one of the own existing activities. This is not testing whether the object
    is acutally deleted - I will do this in an integration test.
    https://stackoverflow.com/questions/11938164/why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
    https://stackoverflow.com/questions/57264115/pytest-and-deleteview
    """
    client = request.getfixturevalue(client_fixture_name)
    django_user_model = request.getfixturevalue(model_fixture_name)
    rf = request.getfixturevalue(request_fixture)
    username = "testuser"
    password = "1234-abcd"

    user = django_user_model.objects.create_user(
        username=username, password=password
    )
    garmin_data = request.getfixturevalue(garmin_fixture_name)
    garmin_data.user = user
    garmin_data.save()
    client.login(username=username, password=password)

    request = rf.post(url)
    request.user = user
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)

    response = delete_activity(request, garmin_data_id=garmin_data.id)

    assert response.status_code == expected_status_code


def test_authenticated_user_can_enter_activities_manually(
    client, django_user_model, rf
):
    """
    this is a test for the view function to add an
    activity manually
    """
    random_username = "testuser"
    random_password = "1234-abcd"
    random_date = date(2023, 8, 31)
    random_steps = 5000
    random_weight = 75
    url = "load_activities_manually"
    expected_status_code = 200

    user = django_user_model.objects.create_user(
        username=random_username, password=random_password
    )
    client.login(username=random_username, password=random_password)
    data = {
        "date": random_date,
        "steps": random_steps,
        "weight": random_weight,
    }

    request = rf.post(url, data=data)
    request.user = user
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    response = load_activities_manually(request)

    assert response.status_code == expected_status_code
    assert GarminData.objects.count() == 1
