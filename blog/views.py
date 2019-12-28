from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView
from django.utils.text import slugify

from .models import Article, Category, Tag

# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    paginate_by = 5


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'next_article': self.object.next_article,
            'prev_article': self.object.prev_article,
        })
        return context


class CategoryView(ArticleListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        self.category_name = category.name
        article_list = Article.objects.filter(category__slug=slug)
        return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'archive_type': '分类',
            'archive_name': self.category_name,
        })
        return context


class TagView(ArticleListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=slug)
        self.tag_name = tag.name
        article_list = Article.objects.filter(tags__slug=slug)
        return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'archive_type': '标签',
            'archive_name': self.tag_name,
        })
        return context


class ArchiveView(ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'article_list'
