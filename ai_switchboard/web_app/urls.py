from django.urls import path, re_path
from . import views

# urlpatterns is a list of route declarations for Django.
# Each path() function defines a route that Django will use to match the requested URL.
urlpatterns = [
    # The path function takes three arguments: 1. A route string that contains a URL pattern. When processing a
    # request, Django starts at the first pattern in urlpatterns and makes its way down the list until it finds a
    # pattern that matches the requested URL. 2. A view function that will be called if the URL pattern matches the
    # requested URL. 3. An optional name for the route that can be used to refer to this route in other parts of
    # Django, such as in templates.
    path('', views.gateway, name='gateway'),  # The home page route. When the URL is empty (i.e., the domain root),
    path('index/', views.landing_page, name='index'),  # The index route. When the URL is 'index/', Django will call

    # Django will call the 'index' view function.
    path('login/', views.user_login, name='login'),  # The login route. When the URL is 'login/', Django will call

    # the 'user_login' view function.
    path('logout/', views.user_logout, name='logout'),  # The logout route. When the URL is 'logout/', Django will

    # call the 'user_logout' view function.

    # 'create_user/', Django will call the 'create_user' view function.
    path('login_required/', views.login_required_view, name='login_required'),

    path('upload_file/', views.upload_file, name='upload_file'),
    path('media/', views.media, name='media'),
    path('delete_file/<int:file_id>/<str:file_type>', views.delete_file, name='delete_file'),

    path('delete_all_files/', views.delete_all_files, name='delete_all_files'), # test

    path('download_file/<int:file_id>/<str:file_type>', views.download_file, name='download_file'),

    path('process_video', views.process_video_view, name='process_video'),
    re_path(r'^process_video/(?P<vid_name>.+)/(?P<processing_model>.*)$', views.process_video_view, name='process_video'),
    path('live-feed/', views.show_live_stream, name='live_feed'),
    path('notifications/', views.emergency_notifications, name='notifications'),
    path('latest_notification/', views.latest_notification, name='latest_notification'),

]
