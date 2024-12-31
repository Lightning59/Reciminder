from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    """ If user is logged in redirect to home page"""
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('index')

    return render(request, 'login_screen.html')