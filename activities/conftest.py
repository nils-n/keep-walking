import pytest
from datetime import date, timedelta
from pytest_factoryboy import register
from .factories import UserFactory, GarmindataFactory
from .models import GarminData

register(UserFactory)
register(GarmindataFactory)


@pytest.fixture()
def garmin_data_list(
    garmindata_factory,
) -> list[GarminData]:
    """
    create a list of fake GarminData objects to test the
    view function that extracts data from the DB
    """
    random_date = date(2023, 8, 31)
    random_steps = 5000
    random_weight = 75

    # create a list of garmin data based on these random values
    number_of_random_dates = 10
    steps_list = [random_steps + i * 50 for i in range(number_of_random_dates)]
    weights_list = [random_weight + i for i in range(number_of_random_dates)]
    date_list = [
        random_date + timedelta(days=i) for i in range(number_of_random_dates)
    ]

    # create the list based on the random values
    data = [
        garmindata_factory.build(
            date=date_list[i], weight_kg=weights_list[i], steps=steps_list[i]
        )
        for i in range(number_of_random_dates)
    ]
    return data
