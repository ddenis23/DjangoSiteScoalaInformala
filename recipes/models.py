from django.conf import settings
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    cooking_time = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="recipes",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="recipe_images/", null=True, blank=True)

    def get_created_at_display(self):
        return self.created_at.strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
