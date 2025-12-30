from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.jobs, name="jobs"),
    path("submit/", views.submit_job, name="submit_job"),
    path("<int:pk>/edit/", views.edit_job, name="edit_job"),
    path("<int:pk>/delete/", views.delete_job, name="delete_job")
]
