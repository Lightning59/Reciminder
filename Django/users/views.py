from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def login_user(request: HttpRequest) -> HttpResponse:
    """Returns a login page, If login is successful or user is already logged in it redirects to home page.
    If user fails at logging in it sends them back to the landing page."""
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('index')

    return render(request, 'login_screen.html')


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    """Logs user out then redirects them back to home page."""
    logout(request)
    return redirect('index')
