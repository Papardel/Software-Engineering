from django.urls import path
from . import views

urlpatterns = [
    path('', views.media, name = 'media'),
    path('upload_file/', views.upload_file, name = 'upload_file'),
    path('delete_file/<int:file_id>/<str:file_type>', views.delete_file, name = 'delete_file'),
    path('download_file/<int:file_id>/<str:file_type>', views.download_file, name = 'download_file'),
]