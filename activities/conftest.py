import pytest
from datetime import date, timedelta
from pytest_factoryboy import register
from .factories import UserFactory, GarmindataFactory
from .models import GarminData

register(UserFactory)
register(GarmindataFactory)


@pytest.fixture()
def garmin_data_list(garmindata_factory) -> list[GarminData]:
    """
    create a list of fake GarminData objects to test the
    view function that extracts data from the DB
    """
    random_date = date(2023, 8, 31)
    number_of_random_dates = 10 
    garmin_data_list = [garmindata_factory.build() for i in range(number_of_random_dates)]
    return garmin_data_list
