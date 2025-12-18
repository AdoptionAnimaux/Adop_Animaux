from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from accounts.views import login_page, register_page, profile_page, admin_dashboard_page, home_page

urlpatterns = [
    path("admin/", admin.site.urls),
    # Main entry point is handled by accounts.urls (root mapping)
    path("", include("accounts.urls")),
]
