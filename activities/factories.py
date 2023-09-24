import factory
from faker import Faker
from django.conf import settings
from .models import GarminData

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory used to create a user in the Foreinkey
    Relationship to the GarminData table
    """

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = fake.name()


class GarmindataFactory(factory.django.DjangoModelFactory):
    """
    Factory to be used during unit testing of
    functions that have GarminData as input parameter
    """

    class Meta:
        model = GarminData

    user = factory.SubFactory(UserFactory)
    steps = fake.random_int(0, 14000)
    weight_kg = fake.random_int(50, 120)
    date = fake.date()
