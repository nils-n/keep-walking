from .models import GarminData


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


def test_garmindata_fixture_works(garmin_data):
    """
    tests that a GarminData instance can be created by this fixture
    """
    model = garmin_data

    assert isinstance(model, GarminData)
