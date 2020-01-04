from django.urls import path

from . import views


app_name = "oauth"

urlpatterns = [
    path('oauth_login', views.oauth_login, name='oauth_login'),
    path('oauth_logout', views.oauth_logout, name='oauth_logout'),
    path('authorize', views.authorize, name='authorize'),
]

