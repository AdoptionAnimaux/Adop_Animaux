from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "service": "adoption_service",
        "endpoints": [
            "/api/client/create/",
            "/api/client/my/",
            "/api/admin/requests/",
            "/api/check/<user>/<animal>/"
        ]
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("adoption.urls")), # All routes without prefix (Traefik strips /adoption)
]
