from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OAuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32, null=True)
    profile_image_url = models.CharField(max_length=256, null=True)

