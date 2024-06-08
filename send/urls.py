from django.urls import path
from . import views

app_name = "send"
urlpatterns = [
    path("", views.file_list, name="file_list"),
    path("upload/", views.file_upload, name="file_upload"),
    path("download/<int:pk>/", views.file_download, name="file_download"),
]