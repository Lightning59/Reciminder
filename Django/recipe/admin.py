from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Recipe

admin.site.register(Recipe)