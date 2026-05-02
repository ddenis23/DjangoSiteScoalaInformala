import os

from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe

RECIPES_PER_PAGE = 5

@login_required
def recipe_list(request):
    recipes = Recipe.objects.order_by("title")
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page = request.GET.get("page")
    recipes_page = paginator.get_page(page)

    context = {
        "recipes": recipes_page,
        "sort": "alpha",
    }
    return render(request, "recipes/recipe_list.html", context)

@login_required
def recipe_list_by_date(request):
    recipes = Recipe.objects.order_by("-created_at")
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page = request.GET.get("page")
    recipes_page = paginator.get_page(page)

    context = {
        "recipes": recipes_page,
        "sort": "date",
    }
    return render(request, "recipes/recipe_list.html", context)

@login_required
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})

@login_required
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect("recipe_detail", id=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, "recipes/recipe_form.html", {"form": form, "action": "Adauga"})

@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, pk=id)

    if recipe.author != request.user:
        messages.error(request, "Nu ai permisiunea sa editezi aceasta reteta.")
        return redirect("recipe_detail", id=recipe.pk)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe_detail", id=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request,
        "recipes/recipe_form.html",
        {"form": form, "action": "Editeaza", "recipe": recipe},
    )


@login_required
def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, pk=id)

    if recipe.author != request.user:
        messages.error(request, "Nu ai permisiunea sa stergi aceasta reteta.")
        return redirect("recipe_detail", id=recipe.pk)

    if request.method == "POST":
        recipe.delete()
        return redirect("recipe_list")

    return render(request, "recipes/recipe_confirm_delete.html", {"recipe": recipe})


@login_required
def recipe_delete_image(request, id):
    recipe = get_object_or_404(Recipe, pk=id)

    if recipe.author != request.user:
        messages.error(request, "Nu ai permisiunea sa stergi imaginea.")
        return redirect("recipe_detail", id=recipe.pk)

    if request.method == "POST":
        if recipe.image:
            if os.path.isfile(recipe.image.path):
                os.remove(recipe.image.path)
            recipe.image = None
            recipe.save()
        return redirect("recipe_detail", id=recipe.pk)

    return render(request, "recipes/recipe_confirm_delete_image.html", {"recipe": recipe})

@login_required
def recipe_search(request):
    query = request.GET.get("query")

    if query is None:
        results = Recipe.objects.all().order_by("title")
    else:
        results = Recipe.objects.filter(title__contains=query).order_by("title")

    paginator = Paginator(results, RECIPES_PER_PAGE)
    page = request.GET.get("page")
    recipes_page = paginator.get_page(page)

    context = {
        "recipes": recipes_page,
        "query": query,
    }
    return render(request, "recipes/recipe_search.html", context)

@login_required
def user_recipes(request, pk):
    profile_user = get_object_or_404(CustomUser, pk=pk)
    recipes = Recipe.objects.filter(author=profile_user).order_by("title")
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page = request.GET.get("page")
    recipes_page = paginator.get_page(page)

    context = {
        "recipes": recipes_page,
        "profile_user": profile_user,
    }
    return render(request, "recipes/user_recipes.html", context)
