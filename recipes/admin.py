from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cooking_time', 'created_at')
    list_filter = ('author',)
    search_fields = ('title', 'description')
    ordering = ('title',)
