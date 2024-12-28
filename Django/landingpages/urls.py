from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.logged_in_home, name='home'),
]