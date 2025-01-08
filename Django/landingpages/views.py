from django.shortcuts import render


def index(request):
    return render(request, 'landing_page.html')
