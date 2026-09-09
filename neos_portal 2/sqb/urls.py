from django.urls import path
from . import views

app_name = "sqb"

urlpatterns = [
    path("", views.job_list, name="list"),
    path("new/", views.job_create, name="create"),
    path("<str:job_number>/", views.job_detail, name="detail"),
    path("<str:job_number>/upload/", views.upload_documents, name="upload"),
    path("<str:job_number>/compile/", views.compile_pdf, name="compile"),
]
