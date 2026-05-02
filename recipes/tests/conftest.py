import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client

from recipes.models import Recipe
User = get_user_model()
@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="pass12345")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="otheruser", password="pass12345")


@pytest.fixture
def logged_in_client(client: Client, user) -> Client:
    client.login(username="testuser", password="pass12345")
    return client


@pytest.fixture
def recipe(user):
    return Recipe.objects.create(
        title="Sarmale",
        description="Reteta traditionala de sarmale.",
        cooking_time="3 ore",
        author=user,
    )
