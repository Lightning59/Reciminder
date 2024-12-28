from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to Reciminder - Bear with us the website is still in development.")
# Create your views here.
