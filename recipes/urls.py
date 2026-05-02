from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("by-date/", views.recipe_list_by_date, name="recipe_list_by_date"),
    path("recipe/add/", views.recipe_add, name="recipe_add"),
    path("recipe/<int:id>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/<int:id>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<int:id>/delete/", views.recipe_delete, name="recipe_delete"),
    path("recipe/<int:id>/delete-image/", views.recipe_delete_image, name="recipe_delete_image"),
    path("search/", views.recipe_search, name="recipe_search"),
    path("user/<int:pk>/recipes/", views.user_recipes, name="user_recipes"),
]
