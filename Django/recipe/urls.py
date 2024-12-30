from django.urls import path

from . import views


urlpatterns = [
    path('addrecipe/', views.add_recipe, name='add-recipe'),
    path('recipe/<str:pk>/', views.view_recipe, name='recipe'),

]