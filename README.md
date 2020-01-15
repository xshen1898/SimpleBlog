# SimpleBlog
使用Django, Bootstrap, jQuery等语言和库编写的一个简单的博客。支持OAuth微博账号登陆评论。

### Demo

<https://www.shenxuchao.cn>

### Environment

+ Docker
    + MySQL
    + Nginx
    + Python3
        + django
        + gunicorn
        + mysqlclient
        + markdown
        + django-uuslug
        + django-haystack
        + whoosh
        + jieba
        + requests

### docker-compose部署过程

```
$ cd /usr/src 
$ mkdir app && cd app
$ git clone https://github.com/xshen1898/SimpleBlog.git
$ cd SimpleBlog/docker
$ docker-compose up -d

$ docker-compose exec mysql bash
$ mysql -u root -p
$ mysql> create database simpleblog;

$ docker-compose exec simpleblog bash
$ python manage.py migrate
$ python manage.py createsuperuser

$ docker-compose exec nginx /usr/local/bin/certbot-auto certonly --nginx
```
