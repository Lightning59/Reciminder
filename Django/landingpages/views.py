from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    """This view just takes any user looking for '/' or index to the plain home landing page."""
    return render(request, 'landing_page.html')
