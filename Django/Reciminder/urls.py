from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('', include("landingpages.urls")),
    path('admin/', admin.site.urls),
    path('account/', include("users.urls")),
    path('recipe/', include("recipe.urls")),
]
