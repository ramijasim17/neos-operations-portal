from django.urls import path
from . import views

app_name = "action_tracker"

urlpatterns = [
    path("", views.action_list, name="list"),
    path("new/", views.action_create, name="create"),
    path("<int:action_id>/", views.action_detail, name="detail"),
]
