from django.urls import path
from django.contrib.auth import views as auth_views
from StudentApp import views as user_view

app_name = 'StudentApp'
urlpatterns = [
    path('homepage/', user_view.homepage_view, name='homepage'),
    path('result-details/', user_view.detail_view, name='details'),
]
