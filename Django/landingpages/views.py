from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'landing_page.html')
# Create your views here.

@login_required
def logged_in_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'logged_in_temp.html', context)
