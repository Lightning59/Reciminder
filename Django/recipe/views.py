from django.shortcuts import render, redirect
from recipe.forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from .models import *


def scrub_invalid_recipe_pk(recipe_pk: str) -> Recipe:
    """Will return the requested recip unless it doesn't exist or was deleted."""
    try:
        recipe = Recipe.objects.get(id=recipe_pk)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    if recipe.deleted_by_user:
        raise Http404("Recipe was deleted")
    return recipe


@login_required(login_url='login')
def add_recipe(request: HttpRequest) -> HttpResponse:
    """Allows the logged-in user to add a recipe sends them to the home screen if successful otherwise back to
     add-recipe. redirects logged-out user to the login screen."""
    form = RecipeForm()
    context = {'form': form}
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add-recipe.html', context)


@login_required(login_url='login')
def view_recipe(request: HttpRequest, pk: str) -> HttpResponse:
    """Displays a specific recipe by its uuid7 pk, if the recipe has the deleted flag or never existed to begin with
    raise a 404 not found error"""
    recipe = scrub_invalid_recipe_pk(pk)
    context = {
        'recipe': recipe,
    }
    return render(request, 'individual_recipe.html', context)


@login_required(login_url='login')
def edit_recipe(request: HttpRequest, pk: str) -> HttpResponse:
    """Allows logged-in users to edit all fields in a recipe (except pk, created-date, modified-date, and is deleted)"""
    recipe = scrub_invalid_recipe_pk(pk)
    form = RecipeForm(instance=recipe)
    context = {
        'recipe': recipe,
        'form': form,
    }
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe', pk=pk)

    return render(request, 'add-recipe.html', context)


@login_required(login_url='login')
def delete_recipe(request: HttpRequest, pk: str) -> HttpResponse:
    """Allows logged-in user to flag the recipe as deleted in the DB. Does not actually delete the recipe from the
     database but flags it as deleted."""
    recipe = scrub_invalid_recipe_pk(pk)
    recipe.deleted_by_user = True
    recipe.save()
    return redirect('home')


# My Current guess for a good default results per page is ~30-40 - anything lower is still experimentation
@login_required(login_url='login')
def logged_in_home(request: HttpRequest, pagination_res_per_page: int = 5) -> HttpResponse:
    """Displays paginated all recipes the user can see or filters down based on simple search algorithm
    Currently just displays all recipes until searched as all users can currently see all recipes
    Accepts pagination as keyword argument with prod default (allows lower to be used in testing)"""
    user = request.user
    all_recipes, search_query = search_recipes(request)

    this_page_recipes, total_pages = paginate_recipes(request, all_recipes, pagination_res_per_page)
    page_range = list(range(1, total_pages + 1))
    context = {'user': user,
               'recipes': this_page_recipes,
               'page_range': page_range,
               'total_pages': total_pages,
               'search_query': search_query}
    return render(request, 'logged_in_temp.html', context)
