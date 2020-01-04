import uuid
from urllib.parse import urlencode

from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .oauth_weibo import OAuthWeibo, OAuthAccessTokenException, OAuthUserInfoException
from .models import OAuthUser


# Create your views here.
def oauth_login(request):
    next_url = request.GET.get('next_url', '/')
    query_string = {
        'client_id': settings.WEIBO_APP_KEY,
        'response_type': 'code',
        'redirect_uri': settings.WEIBO_REDIRECT_URI,
        'state': next_url,
    }
    url = 'https://api.weibo.com/oauth2/authorize?{}'.format(urlencode(query_string))
    
    return HttpResponseRedirect(url)


def authorize(request):
    next_url = request.GET.get('state', '/')
    code = request.GET.get('code', None)
    owb = OAuthWeibo(settings.WEIBO_APP_KEY, settings.WEIBO_APP_SECRET, settings.WEIBO_REDIRECT_URI)
    try:
        token = owb.get_access_token(code)
    except OAuthAccessTokenException as e:
        return HttpResponseRedirect('/')
    user = User.objects.filter(username=token['uid']).first()
    if user is not None:
        login(request, user)
    else:
        try:
            owb_user = owb.get_user_info(token)
        except OAuthUserInfoException as e:
            return HttpResponseRedirect('/')
        new_user = User(username=owb_user['id'])
        pwd = str(uuid.uuid1())
        new_user.set_password(pwd)
        new_user.save()
        oauth_user = OAuthUser(user=new_user, nickname=owb_user['name'], profile_image_url=owb_user['profile_image_url'])
        oauth_user.save()
        login(request, new_user)
    
    return HttpResponseRedirect(next_url)


def oauth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

