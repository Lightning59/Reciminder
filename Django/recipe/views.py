from django.shortcuts import render, redirect
from recipe.forms import RecipeForm
from django.contrib.auth.decorators import login_required


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
