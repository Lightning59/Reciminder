from django.shortcuts import render, redirect
from recipe.forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from .models import Recipe


@login_required(login_url='login')
def add_recipe(request):
    form = RecipeForm()
    context = {'form': form}
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'add-recipe.html', context)


@login_required(login_url='login')
def view_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if recipe.deleted_by_user:
        # TODO play around with this in a prod environment I think I can explicitly say WAS DELTED here without leaking info but need to check.
        raise Http404("Recipe does not exist or was deleted")
    context={
        'recipe': recipe,
    }
    return render(request, 'individual_recipe.html', context)


@login_required(login_url='login')
def edit_recipe(request, pk):

    recipe = Recipe.objects.get(id=pk)
    if recipe.deleted_by_user:
        # TODO play around with this in a prod environment I think I can explicitly say WAS DELTED here without leaking info but need to check.
        raise Http404("Recipe does not exist or was deleted")

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
def delete_recipe(request, pk):
    # TODO: These need to implement flash messages to help the user now if it was successful or not
    recipe = Recipe.objects.get(id=pk)
    recipe.deleted_by_user = True
    recipe.save()
    return redirect('home')


@login_required(login_url='login')
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