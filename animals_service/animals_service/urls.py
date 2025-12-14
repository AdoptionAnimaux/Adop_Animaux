from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "service": "animals_service",
        "endpoints": [
            "/api/animals/",
            "/api/admin/animals/..."
        ]
    })


urlpatterns = [
    path('animals/', include('animals.urls')), # For Traefik /animals/ routing
    path('', include('animals.urls')), # Custom URLs first to catch 'admin/animals/'
    path('admin/', admin.site.urls),
]
