from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User

from .models import Comment, Discussion
from blog.models import Article

# Create your views here.
def create_comment(request, article_id):
    if request.method == "POST":
        user = request.user
        content = request.POST.get('comment', '')
        article = Article.objects.get(pk=article_id)
        url = article.get_absolute_url()
        if user.is_authenticated:
            comment = Comment(content=content, user=user, article=article)
            comment.save()
            url = '{}#comment_{}'.format(url, comment.pk)
        return HttpResponseRedirect(url)


def create_discussion(request):
    if request.method == "POST":
        user = request.user
        content = request.POST.get('comment', '')
        comment_id = request.POST.get('comment_id', '')
        to_user_id = request.POST.get('to_user_id', '')
        comment = Comment.objects.get(pk=comment_id)
        to_user = User.objects.get(pk=to_user_id)
        url = comment.article.get_absolute_url()
        if user.is_authenticated:
            discussion = Discussion(comment=comment, content=content, user=user, to_user=to_user)
            discussion.save()
            url = '{}#discussion_{}'.format(url, discussion.pk)
        return HttpResponseRedirect(url)

