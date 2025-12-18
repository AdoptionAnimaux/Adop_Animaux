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
    path('', include('animals.urls')), # All routes without prefix (Traefik strips /animals)
    path('admin/', admin.site.urls),
]
