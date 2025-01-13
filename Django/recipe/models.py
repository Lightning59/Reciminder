from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.db.models import Q
from django.db.models.query import QuerySet
import uuid6
from django.http import HttpRequest


class Recipe(models.Model):
    """Recipe model captures user recipes."""
    id = models.UUIDField(primary_key=True, default=uuid6.uuid7, unique=True, editable=False)
    # test long recipe title - Came to ~100. So pick 255(256?) as a good permissive limit?
    title=models.CharField(max_length=255, null=False, blank=False)
    description_free_text=models.TextField(null=True, blank=True)
    ingredients_free_text=models.TextField(null=True, blank=True)
    instructions_free_text=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    deleted_by_user=models.BooleanField(default=False)
    servings_per_nominal=models.FloatField(null=True, blank=True)
    original_website_link=models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        """Just returns the full recipe title as a string."""
        return self.title

    class Meta:
        ordering=['-created']


def paginate_recipes(request:HttpRequest, recipes:QuerySet, num_results_per_page:int) ->tuple[Page,int]:
    """Paginate a passed queryset - with specified number of results per page."""
    curr_page = request.GET.get('page')
    paginator = Paginator(recipes, num_results_per_page)
    total_pages = paginator.num_pages
    try:
        page_recipes = paginator.page(curr_page)
    except PageNotAnInteger:
        curr_page = 1
        page_recipes = paginator.page(curr_page)
    except EmptyPage:
        curr_page = total_pages
        page_recipes = paginator.page(curr_page)
    return page_recipes, total_pages


def search_recipes(request: HttpRequest) -> tuple[QuerySet, str | None]:
    """Basic search that matches all text fields in the recipes model"""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        recipes = Recipe.objects.filter(deleted_by_user=False).filter(
            Q(title__icontains=search_query) |
            Q(description_free_text__icontains=search_query) |
            Q(instructions_free_text__icontains=search_query) |
            Q(ingredients_free_text__icontains=search_query) |
            Q(original_website_link__icontains=search_query))
    else:
        recipes = Recipe.objects.filter(deleted_by_user=False).all()
        search_query = ''

    return recipes, search_query
