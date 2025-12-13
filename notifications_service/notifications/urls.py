from django.urls import path
from . import views

urlpatterns = [
    path("notifications/", views.notifications_home, name="notifications_home"),
    path("health/", views.health, name="health"),
    path("my/", views.my_notifications, name="my_notifications"),
    path("user/<int:user_id>/", views.user_notifications, name="user_notifications"),

]
