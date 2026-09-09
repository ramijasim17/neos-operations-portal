from django.urls import path
from . import views

app_name = "daily_report"

urlpatterns = [
    path("", views.report_list, name="list"),
    path("new/", views.report_create, name="create"),
    path("<int:report_id>/edit/", views.report_edit, name="edit"),
    path("<int:report_id>/delete/", views.report_delete, name="delete"),
]
