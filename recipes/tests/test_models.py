import re

import pytest

from recipes.models import Recipe


@pytest.mark.django_db
def test_recipe_str(user):
    recipe = Recipe.objects.create(
        title="Papanasi",
        description="Cu smantana si dulceata.",
        cooking_time="20 minute",
        author=user,
    )
    assert str(recipe) == "Papanasi"


@pytest.mark.django_db
def test_recipe_author_relation(user):
    recipe = Recipe.objects.create(
        title="Cozonac",
        description="Pufos si gustos.",
        cooking_time="2 ore",
        author=user,
    )
    assert recipe.author == user
    assert recipe in user.recipes.all()


@pytest.mark.django_db
def test_get_created_at_display_format(user):
    recipe = Recipe.objects.create(
        title="Placinta cu mere",
        description="Delicioasa.",
        cooking_time="1 ora",
        author=user,
    )
    result = recipe.get_created_at_display()
    assert re.match(r"^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$", result)


@pytest.mark.django_db
def test_recipe_default_ordering_is_alphabetical(user):
    Recipe.objects.create(title="Zupa", description=".", cooking_time="1h", author=user)
    Recipe.objects.create(title="Alivenci", description=".", cooking_time="1h", author=user)
    Recipe.objects.create(title="Mici", description=".", cooking_time="1h", author=user)

    titles = list(Recipe.objects.values_list("title", flat=True))
    assert titles == sorted(titles)
