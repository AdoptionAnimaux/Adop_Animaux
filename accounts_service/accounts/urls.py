from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # Auth (Standard SimpleJWT + Custom Login wrapper if needed, 
    # but strictly implementing the requested views)
    path('', views.login_page, name='root_login'),
    path('login/', views.login_page, name='ui_login'),
    path('register/', views.register_page, name='ui_register'),
    path('profile/', views.profile_page, name='ui_profile'),
    path('admin-panel/', views.admin_dashboard_page, name='ui_admin_dashboard'),
    path('home/', views.home_page, name='ui_home'),

    # Auth API
    path('api/login/', views.login_view, name='login'),
    path('api/register/', views.register, name='register'),
    
    # Token Standard Endpoints (Optional but good practice)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User
    path('api/me/', views.current_user, name='current_user'),
    path('api/delete-account/', views.delete_account, name='delete_account'),

    # Admin
    path('api/admin-panel/users/', views.admin_list_users, name='admin_list_users'),
    path('api/admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('api/admin-panel/users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),

    # Health
    path('health/', views.health, name='health'),
]
