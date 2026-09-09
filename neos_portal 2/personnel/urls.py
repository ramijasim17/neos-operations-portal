from django.urls import path
from . import views

app_name = "personnel"

urlpatterns = [
    path("", views.personnel_list, name="list"),
    path("new/", views.personnel_create, name="create"),
    path("<int:person_id>/edit/", views.personnel_edit, name="edit"),
    path("<int:person_id>/delete/", views.personnel_delete, name="delete"),
]
