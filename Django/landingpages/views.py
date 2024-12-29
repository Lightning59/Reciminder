from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recipe.models import Recipe


def index(request):
    return render(request, 'landing_page.html')
# Create your views here.

@login_required
def logged_in_home(request):
    user = request.user
    all_recipes = Recipe.objects.all()
    context = {'user': user, 'recipes': all_recipes}
    return render(request, 'logged_in_temp.html', context)
