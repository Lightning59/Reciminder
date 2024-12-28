from django.http import HttpResponse


def index(request):
    return HttpResponse("<!DOCTYPE html><html><head><title>Reciminder</title></head><body><h1>Welcome to Reciminder!</h1><p>Bear with us the website is still in development.</p></body></html>")
# Create your views here.
