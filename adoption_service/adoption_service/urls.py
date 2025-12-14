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
    path("api/", include("adoption.urls")),
    path("adoption/api/", include("adoption.urls")), # Handle /adoption/api/...
    path("adoption/", include("adoption.urls")), # Expose UI under /adoption/... (e.g. /adoption/create/)
    path("", root_view),
]
