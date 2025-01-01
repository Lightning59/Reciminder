from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recipe.models import Recipe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):
    return render(request, 'landing_page.html')
# Create your views here.

@login_required
def logged_in_home(request):
    user = request.user
    all_recipes, search_query = search_recipes(request)
    # My Current guess for a good deafult results for page is 30 - anything lower is still experimentation
    this_page_recipes, total_pages = paginate_recipes(request, all_recipes, 4)
    page_range=list(range(1, total_pages+1))
    context = {'user': user,
               'recipes': this_page_recipes,
               'page_range': page_range,
               'total_pages': total_pages,
               'search_query': search_query}
    return render(request, 'logged_in_temp.html', context)


def paginate_recipes(request, recipes, num_results_per_page):
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


def search_recipes(request):
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        recipes = Recipe.objects.filter(deleted_by_user=False).filter(
                                        Q(title__icontains=search_query) |
                                        Q(description_free_text__icontains=search_query)|
                                        Q(ingredients_free_text=search_query)|
                                        Q(ingredients_free_text__icontains=search_query)|
                                        Q(original_website_link__icontains=search_query))
    else:
        recipes = Recipe.objects.filter(deleted_by_user=False).all()
        search_query = ''

    return recipes, search_query