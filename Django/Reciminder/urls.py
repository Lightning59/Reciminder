from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', include("landingpages.urls")),
    path('admin/', admin.site.urls),
    path('account/', include("users.urls")),
    path('recipe/', include("recipe.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)