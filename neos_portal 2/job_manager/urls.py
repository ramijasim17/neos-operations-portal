from django.urls import path
from . import views

app_name = "job_manager"

urlpatterns = [
    path("", views.job_list, name="list"),
    path("new/", views.job_create, name="create"),
    path("<int:job_id>/edit/", views.job_edit, name="edit"),
    path("<int:job_id>/delete/", views.job_delete, name="delete"),
]
