from django.urls import path
from . import views

app_name = "maintenance"

urlpatterns = [
    path("", views.record_list, name="list"),
    path("new/", views.record_create, name="create"),
    path("<int:record_id>/edit/", views.record_edit, name="edit"),
    path("<int:record_id>/delete/", views.record_delete, name="delete"),
    path("levels/", views.manage_levels, name="manage_levels"),
]
