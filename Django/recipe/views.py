from django.shortcuts import render, redirect
from recipe.forms import RecipeForm
from django.contrib.auth.decorators import login_required
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