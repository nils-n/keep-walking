import pytest
from pytest_factoryboy import register
from .factories import UserFactory, GarmindataFactory

register(UserFactory)
register(GarmindataFactory)
