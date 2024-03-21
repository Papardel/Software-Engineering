from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Change 'home' to 'index'
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_user/', views.create_user, name='create_user'),
    path('update_password/', views.update_password, name='update_password'),
]