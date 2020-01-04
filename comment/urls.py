from django.urls import path

from . import views


app_name = "comment"

urlpatterns = [
    # ex: /blog/
    path('create_comment/<int:article_id>/', views.create_comment, name='create_comment'),
    path('create_discussion', views.create_discussion, name='create_discussion'),
]
