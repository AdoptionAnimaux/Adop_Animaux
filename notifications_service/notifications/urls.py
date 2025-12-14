from django.urls import path
from . import views

urlpatterns = [
    path("notifications/", views.ui_notifications_list, name="ui_notifications"), # UI
    path("api/notifications/", views.my_notifications, name="my_notifications"),
    path("health/", views.health, name="health"),
]
