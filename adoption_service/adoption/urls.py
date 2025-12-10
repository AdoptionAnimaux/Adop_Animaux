from django.urls import path
from . import views

urlpatterns = [

    # ---------------------------------------------
    # 👤 CLIENT ROUTES
    # ---------------------------------------------
    path("", views.home, name="adoption_home"),
    path("create/", views.create_request, name="create_adoption"),
    path("list/<int:user_id>/", views.user_requests, name="user_adoptions"),
    path("status/<int:id>/", views.request_status, name="request_status"),
    path("cancel/<int:id>/", views.cancel_request, name="cancel_request"),

    # ---------------------------------------------
    # 👨‍💼 ADMIN ROUTES
    # ---------------------------------------------
    path("admin/requests/", views.admin_list, name="admin_requests"),
    path("admin/approve/<int:id>/", views.approve_request, name="approve_request"),
    path("admin/reject/<int:id>/", views.reject_request, name="reject_request"),
]
