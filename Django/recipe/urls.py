from django.urls import path

from . import views


urlpatterns = [
    path('addrecipe/', views.add_recipe, name='add-recipe'),
    path('view/<str:pk>/', views.view_recipe, name='recipe'),
    path('edit/<str:pk>/', views.edit_recipe, name='edit-recipe'),

    path('delete/<str:pk>/', views.delete_recipe, name='delete-recipe'),

]