from django.core.exceptions import ValidationError
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.db.models import Q
from django.db.models.query import QuerySet
import uuid6
from django.http import HttpRequest


def validate_positive_float(value):
    if value < 0:
        raise ValidationError("Negative values are not allowed")

class Recipe(models.Model):
    """Recipe model captures user recipes."""
    id = models.UUIDField(primary_key=True, default=uuid6.uuid7, unique=True, editable=False)

    # test long recipe title - Came to ~100. So pick 255(256?) as a good permissive limit?
    title=models.CharField(max_length=255, null=False, blank=False)

    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    deleted_by_user=models.BooleanField(default=False)

    description_free_text = models.TextField(null=True, blank=True)
    ingredients_free_text = models.TextField(null=True, blank=True)
    instructions_free_text = models.TextField(null=True, blank=True)
    notes_free_text = models.TextField(null=True, blank=True)
    nutrition_free_text = models.TextField(null=True, blank=True)

    original_website_link=models.URLField(null=True, blank=True)

    servings_per_nominal = models.FloatField(null=True, blank=True, validators=[validate_positive_float])

    pre_prep_active_time_minutes=models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    prep_active_time_minutes = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    cook_active_time_minutes = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    clean_active_time_minutes = models.PositiveSmallIntegerField(null=False, blank=True, default=0)

    pre_prep_passive_time_minutes=models.PositiveIntegerField(null=False, blank=True, default=0)
    cook_passive_time_minutes=models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    after_cook_passive_time_minutes=models.PositiveIntegerField(null=False, blank=True, default=0)

    total_active_time_minutes=models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    total_passive_time_minutes=models.PositiveIntegerField(null=False, blank=True, default=0)
    total_overall_time_minutes=models.PositiveIntegerField(null=False, blank=True, default=0)


    class Meta:
        ordering=['-created']

    def __str__(self) -> str:
        """Just returns the full recipe title as a string."""
        return self.title

    def calc_and_store_times(self):
        self.total_active_time_minutes=(self.pre_prep_active_time_minutes
                                        + self.prep_active_time_minutes
                                        + self.cook_active_time_minutes
                                        + self.clean_active_time_minutes)
        self.total_passive_time_minutes=(self.pre_prep_passive_time_minutes
                                         + self.cook_passive_time_minutes
                                         + self.after_cook_passive_time_minutes)
        self.total_overall_time_minutes=(self.total_active_time_minutes + self.total_passive_time_minutes)




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
            Q(notes_free_text__icontains=search_query) |
            Q(original_website_link__icontains=search_query))
    else:
        recipes = Recipe.objects.filter(deleted_by_user=False).all()
        search_query = ''

    return recipes, search_query
