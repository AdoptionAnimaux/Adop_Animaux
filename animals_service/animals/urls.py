from django.urls import path
from . import views

urlpatterns = [
    # UI
    path("", views.catalog_view, name="ui_catalog"),
    path('admin/animals/', views.admin_page, name='ui_admin_animals'),

    # API (REST)
    path("api/animals/", views.AnimalListCreateAPI.as_view(), name="api_animals"),
    path("api/animals/<int:pk>/", views.AnimalRetrieveUpdateDestroyAPI.as_view(), name="api_animal_detail"),
    path("api/animals/<int:pk>/adopt/", views.request_adoption_api, name="api_animal_adopt"),

    # Admin API
    path("api/admin/animals/<int:pk>/approve/", views.approve_animal_api, name="approve_animal"),
    path("api/admin/animals/<int:pk>/reject/", views.reject_animal_api, name="reject_animal"),
]
