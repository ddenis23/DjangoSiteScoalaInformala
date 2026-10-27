# Recipe Manager — Django Web App

A multi-user web application for publishing and managing cooking recipes, built with **Django** as the final project of the Python Developer program at Scoala Informala de IT. The interface is in Romanian.

## Features

- **User accounts** — registration, login and logout with a custom user model (`accounts` app)
- **Recipes CRUD** — create, view, edit and delete recipes (title, description, cooking time, optional photo)
- **Ownership rules** — only the author of a recipe can edit or delete it, or remove its image
- **Image upload** — recipe photos stored as media files (Pillow)
- **Browsing** — alphabetical list or newest first, with pagination
- **Search** — find recipes by title
- **Author pages** — see all recipes published by a specific user
- **Automated tests** — pytest + pytest-django tests for the `Recipe` model

## Tech stack

- Python 3, Django 6
- SQLite (development database)
- Django templates, HTML5, CSS3
- Pillow for image handling
- pytest, pytest-django

## Getting started

```bash
git clone https://github.com/ddenis23/DjangoSiteScoalaInformala.git
cd DjangoSiteScoalaInformala
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Running the tests

```bash
pytest
```

## Project structure

```
retete_project/   # project settings and root URLs
accounts/         # custom user model, login / register / logout views
recipes/          # Recipe model, views, forms, templates, static CSS
recipes/tests/    # pytest tests and fixtures (conftest.py)
```

## Notes

This is a learning project configured for local development (`DEBUG = True`, SQLite, development secret key). For a production deployment the secret key and debug settings would be moved to environment variables.
