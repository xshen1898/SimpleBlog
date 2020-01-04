import requests
import json


class OAuthAccessTokenException(Exception):
    '''
    Authorization failed.
    '''


class OAuthWeibo(object):
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_access_token(self, code):
        url = 'https://api.weibo.com/oauth2/access_token'

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(url, data=payload)
        result = json.loads(response.text)

        if 'uid' not in result or 'access_token' not in result:
            raise OAuthAccessTokenException(response.text)

        return result

    def get_user_info(self, token):
        url = 'https://api.weibo.com/2/users/show.json'

        payload = {
            'uid': token['uid'],
            'access_token': token['access_token']
        }

        response = requests.get(url, params=payload)

        return json.loads(response.text)

