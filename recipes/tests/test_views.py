import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse

from recipes.models import Recipe

User = get_user_model()

@pytest.mark.django_db
def test_login_page_loads(client: Client):
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_valid(client: Client, user):
    response = client.post(reverse("login"), {
        "username": "testuser",
        "password": "pass12345",
    })
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_login_invalid(client: Client, db):
    response = client.post(reverse("login"), {
        "username": "utilizator_inexistent",
        "password": "parola_gresita",
    })
    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_register(client: Client, db):
    response = client.post(reverse("register"), {
        "username": "user_nou",
        "password1": "parola_noua_123",
        "password2": "parola_noua_123",
    })
    assert response.status_code == 302
    assert User.objects.filter(username="user_nou").exists()


@pytest.mark.django_db
def test_unauthenticated_redirected_from_add(client: Client, db):
    response = client.get(reverse("recipe_add"))
    assert response.status_code == 302
    assert "login" in response.url

@pytest.mark.django_db
def test_create_recipe_authenticated(logged_in_client: Client):
    response = logged_in_client.post(reverse("recipe_add"), {
        "title": "Ciorba de burta",
        "description": "O ciorba delicioasa.",
        "cooking_time": "2 ore",
    })
    assert response.status_code == 302
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_create_recipe_unauthenticated(client: Client, db):
    client.post(reverse("recipe_add"), {
        "title": "Reteta fara login",
        "description": "Nu ar trebui salvata.",
        "cooking_time": "1 ora",
    })
    assert Recipe.objects.count() == 0


@pytest.mark.django_db
def test_edit_recipe_by_owner(logged_in_client: Client, recipe: Recipe):
    response = logged_in_client.post(
        reverse("recipe_edit", args=[recipe.pk]),
        {
            "title": "Sarmale cu varza acra",
            "description": "Reteta actualizata.",
            "cooking_time": "4 ore",
        }
    )
    assert response.status_code == 302
    recipe.refresh_from_db()
    assert recipe.title == "Sarmale cu varza acra"


@pytest.mark.django_db
def test_edit_recipe_by_non_owner(client: Client, other_user, recipe: Recipe):
    client.login(username="otheruser", password="pass12345")
    client.post(
        reverse("recipe_edit", args=[recipe.pk]),
        {
            "title": "Titlu modificat de altcineva",
            "description": ".",
            "cooking_time": "1h",
        }
    )
    recipe.refresh_from_db()
    assert recipe.title == "Sarmale"


@pytest.mark.django_db
def test_delete_recipe_by_owner(logged_in_client: Client, recipe: Recipe):
    response = logged_in_client.post(reverse("recipe_delete", args=[recipe.pk]))
    assert response.status_code == 302
    assert Recipe.objects.count() == 0


@pytest.mark.django_db
def test_delete_recipe_by_non_owner(client: Client, other_user, recipe: Recipe):
    client.login(username="otheruser", password="pass12345")
    client.post(reverse("recipe_delete", args=[recipe.pk]))
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_recipe_detail_visible_without_login(client: Client, recipe: Recipe):
    response = client.get(reverse("recipe_detail", args=[recipe.pk]))
    assert response.status_code == 200
    assert b"Sarmale" in response.content

@pytest.mark.django_db
def test_recipe_list_sorted_alphabetically(client: Client, user):
    Recipe.objects.create(title="Zacusca", description=".", cooking_time="2h", author=user)
    Recipe.objects.create(title="Ardei umpluti", description=".", cooking_time="1h", author=user)
    Recipe.objects.create(title="Mamaliga", description=".", cooking_time="30 min", author=user)

    response = client.get(reverse("recipe_list"))
    recipes = list(response.context["recipes"])
    titles = [r.title for r in recipes]
    assert titles == sorted(titles)


@pytest.mark.django_db
def test_recipe_list_sorted_by_date(client: Client, user):
    from django.utils import timezone

    Recipe.objects.create(title="Prima reteta", description=".", cooking_time="1h", author=user, created_at=timezone.now())
    Recipe.objects.create(title="A doua reteta", description=".", cooking_time="1h", author=user, created_at=timezone.now())

    response = client.get(reverse("recipe_list_by_date"))
    recipes = list(response.context["recipes"])
    dates = [r.created_at for r in recipes]
    assert dates == sorted(dates, reverse=True)
