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
    path("", include("notifications.urls")),
]
