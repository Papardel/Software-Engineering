from django.urls import path
from . import views

# urlpatterns is a list of route declarations for Django.
# Each path() function defines a route that Django will use to match the requested URL.
urlpatterns = [
    # The path function takes three arguments: 1. A route string that contains a URL pattern. When processing a
    # request, Django starts at the first pattern in urlpatterns and makes its way down the list until it finds a
    # pattern that matches the requested URL. 2. A view function that will be called if the URL pattern matches the
    # requested URL. 3. An optional name for the route that can be used to refer to this route in other parts of
    # Django, such as in templates.
    path('', views.index, name='index'),  # The home page route. When the URL is empty (i.e., the domain root),
    # Django will call the 'index' view function.
    path('login/', views.user_login, name='login'),  # The login route. When the URL is 'login/', Django will call
    # the 'user_login' view function.
    path('logout/', views.user_logout, name='logout'),  # The logout route. When the URL is 'logout/', Django will
    # call the 'user_logout' view function.
    path('create_user/', views.create_user, name='create_user'),  # The creation user route. When the URL is
    # 'create_user/', Django will call the 'create_user' view function.
    path('update_password/', views.update_password, name='update_password'),  # The update password route. When the
    # URL is 'update_password/', Django will call the 'update_password' view function.
]