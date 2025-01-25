from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Recipe, RecipeImage

admin.site.register(Recipe)
admin.site.register(RecipeImage)