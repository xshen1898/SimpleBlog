from django.urls import path

from . import views


app_name = "blog"

urlpatterns = [
    # ex: /blog/
    path('', views.ArticleListView.as_view(), name='index'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('archive', views.ArchiveView.as_view(), name='archive'),
]
