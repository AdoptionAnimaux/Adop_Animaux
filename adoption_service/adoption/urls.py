from django.urls import path
from . import views

urlpatterns = [
    # UI
    path("create/", views.creation_page, name="ui_create_request"),
    path("my/", views.my_list_page, name="ui_my_requests"),
    path("admin-panel/", views.admin_page, name="ui_admin_requests"),

    # Client
    path("client/create/", views.create_request, name="create_request"),
    path("client/my/", views.user_requests, name="user_requests"),
    path("client/<int:id>/status/", views.request_status, name="request_status"),
    path("client/<int:id>/cancel/", views.cancel_request, name="cancel_request"),

    # Admin
    path("admin-panel/requests/", views.admin_list, name="admin_list"),
    path("admin-panel/requests/<int:id>/approve/", views.approve_request, name="approve_request"),
    path("admin-panel/requests/<int:id>/reject/", views.reject_request, name="reject_request"),

    # Inter-service
    path("check/<int:user_id>/<int:animal_id>/", views.check_adoption, name="check_adoption"),
    path("health/", views.health, name="health"),
]
