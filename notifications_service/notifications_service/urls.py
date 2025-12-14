from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "service": "notifications_service",
        "endpoints": [
            "/api/notifications/",
            "/health/"
        ]
    })

urlpatterns = [
    path("", root_view),
    # App urls are mapped to root, so it becomes /api/notifications/
    path("notifications/", include("notifications.urls")),
    path("", include("notifications.urls")),
]
