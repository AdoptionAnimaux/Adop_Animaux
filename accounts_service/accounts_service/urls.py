from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from accounts.views import login_page, register_page, profile_page, admin_dashboard_page, home_page

urlpatterns = [
    # UI Routes
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
    path("profile/", profile_page, name="profile_page"),
    path("admin-panel/", admin_dashboard_page, name="admin_dashboard"),
    path("home/", home_page, name="home_page"),
    
    path("admin/", admin.site.urls),
    path("", login_page, name="root_login"), # Main entry point is Login
    
    # Traefik Prefix Routes
    path("accounts/login/", login_page),
    path("accounts/register/", register_page),
    path("accounts/profile/", profile_page),
    path("accounts/admin-panel/", admin_dashboard_page),
    path("accounts/home/", home_page),
    path("accounts/", include("accounts.urls")),

    # API Routes
    path("", include("accounts.urls")),
]
