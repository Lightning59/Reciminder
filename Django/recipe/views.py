from django.shortcuts import render, redirect
from recipe.forms import RecipeForm
from django.contrib.auth.decorators import login_required
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
    context={
        'recipe': recipe,
    }
    return render(request, 'individual_recipe.html', context)


@login_required(login_url='login')
def edit_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
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
